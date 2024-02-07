import requests
import subprocess
import os
import sys

OPTIMISM_URL = "https://witnesschain-l2-snapshots.s3.amazonaws.com/op-latest"
BASE_URL = "https://witnesschain-l2-snapshots.s3.amazonaws.com/base-latest"
GIT_URL = "https://github.com/ethereum-optimism/optimism.git"
GIT_GETH_URL = "https://github.com/ethereum-optimism/op-geth.git"
CHUNK_SIZE = 100*1024*1024 # using chunk size of 100 MB for state download

def download_file(url, local_file_path):
    local_filename = url.split('/')[-1]
    local_filename = local_file_path + "/" +  local_filename
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        size = int(r.headers.get("Content-length"))
        downloaded_size = 0

        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                downloaded_size += len(chunk)
                f.write(chunk)

    if downloaded_size != size:
        return False, local_filename

    return True, local_filename

if len(sys.argv) != 3:
    print("Number of argument is 2")
    print("1st argument: 84532/11155420 (84532 for base-sepolia, 11155420 for op-sepolia)")
    print("2nd argument: L1_RPC_URL, example: https://eth-sepolia.g.alchemy.com/v2/hhTXZSBtLsbNN-wXWpErThgYi9sNNKTP")
    sys.exit(1)


script_directory = sys.argv[0]
chain_id = sys.argv[1]
l1_rpc_url = sys.argv[2]

script_directory = "./"
DOWNLOAD_URL = ""

try:
    chain_id = int(chain_id)
except:
    print("Argument to the script must be integer")
    sys.exit(1)

if chain_id == 84532:
    DOWNLOAD_URL = BASE_URL
elif chain_id == 11155420:
    DOWNLOAD_URL = OPTIMISM_URL
else:
    print("Unknown chain id " + str(chain_id) + ". Valid chain ids are 84532 for base-sepolia, 11155420 for op-sepolia.")

DOWNLOAD_URL = subprocess.check_output(['curl', DOWNLOAD_URL]).decode().strip()

print("Starting download. URL:", DOWNLOAD_URL, "Local file path:", script_directory)

while True:
    file_downloaded, local_filename = download_file(DOWNLOAD_URL, script_directory)
    if file_downloaded:
        break
    print("Download failed. Retrying.")

print("Download completed!!")

print("Untarring snapshot")
subprocess.run(["tar", "xzf", local_filename, "-C", script_directory])
print("Untar successful!!")

print('Cloning optimism git repo for optimism')

subprocess.run(["rm", "-rf", script_directory + '/optimism'])
subprocess.run(["git", "clone", GIT_URL, script_directory + '/optimism'])

os.chdir(script_directory + "/optimism")
subprocess.run(["git", "checkout", "op-node/v1.4.0"])
print("Running pnpm install")
subprocess.run(["pnpm", "install"])
print("Running pnpm build")
subprocess.run(["pnpm", "build"])
print("Running make op-node")
subprocess.run(["make", "op-node"])
print("Building op-geth")
subprocess.run(["git", "clone", GIT_GETH_URL])
f = open("jwt.txt", "w")
subprocess.run(["openssl", "rand", "-hex", "32"], stdout=f)
f.close()
subprocess.run(["cp", "jwt.txt", "op-geth/"])
subprocess.run(["cp", "jwt.txt", "op-node/"])
subprocess.run(["mkdir", "op-geth/datadir"])

os.chdir("../")

geth_script = ""
node_script = ""
geth_terminal_name = ""
node_terminal_name = ""

if chain_id == 84532:
    geth_script = "run-geth-base.sh"
    node_script = "run-node-base.sh"
    geth_terminal_name = "base-geth"
    node_terminal_name = "base-node"
elif chain_id == 11155420:
    geth_script = "run-geth-optimism.sh"
    node_script = "run-node-optimism.sh"
    geth_terminal_name = "optimism-geth"
    node_terminal_name = "optimism-node"


subprocess.run(["mv", "geth", "optimism/op-geth/datadir/"])
subprocess.run(["cp", geth_script, "optimism/op-geth/"])
subprocess.run(["cp", node_script, "optimism/op-node/"])
subprocess.run(["git", "checkout", node_script])
subprocess.run(["sed", "-i", "s,<L1_RPC_URL>," + l1_rpc_url + ",", "optimism/op-node/" + node_script])


os.chdir("optimism/op-geth")
subprocess.run(["git", "checkout", "v1.101304.2"])
print("Compiling op-geth")
subprocess.run(["make", "geth"])
print("Compiled op-geth")
#start geth 
subprocess.run(["tmux","new-session", "-d", "-s", geth_terminal_name, "./" + geth_script])
print("Started op-geth")

os.chdir("../../optimism/op-node")

#start node
subprocess.run(["tmux","new-session", "-d", "-s", node_terminal_name, "./" + node_script])
print("Started op-geth")
