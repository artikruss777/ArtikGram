# ArtikGram

<p align="center">
  <img src="assets/icons/logo.jpg" alt="ArtikGram Logo" width="200" height="200">
</p>

<h3 align="center">The Next-Generation Telegram Client</h3>
<p align="center">Powered by Python, Kivy, and Artificial Intelligence</p>

<p align="center">
  <!-- Замени ссылки ниже, когда появится проект -->
  <a href="https://t.me/artikgram">Telegram Channel</a> •
  <a href="mailto:artembahanov156@gmail.com">Contact Me</a>
</p>

---

**⚠️ Important Notice: Project in Early Development**

Hey there! Welcome to the ArtikGram GitHub repository. This is a very ambitious project to create a feature-rich, AI-powered Telegram client from the ground up.

Please be aware that this project is in its **very early stages**. Right now, it's more of a proof-of-concept with a basic UI. A lot of the cool features are in the planning and design phase.

I'm learning as I build, so any help, advice, or encouragement is greatly appreciated!

### 🚧 Current Status

*   **What's working:** A welcome screen and a phone number input prototype (non-functional UI).
*   **What's not working:** Almost everything else! This is a skeleton right now.
*   **Build guide:** Not available yet. I'll write one once there's something substantial to build.

### 🧠 Planned AI-Powered Features (The Dream List)

The ultimate goal for ArtikGram is to integrate cutting-edge AI to make your messaging smarter:
*   **AI Assistant & Chat Summarization**
*   **Advanced Anti-Spam**
*   **Smart Reply & Content Generation**
*   **Voice & Speech Features** (TTS, STT, Voice Changer)
*   **User Analytics & Statistics**
*   ...and much more.

### 👨‍💻 About the Developer

Hi! I'm **Artem** (`@artikruss777`). I'm 12 years old and I'm passionate about programming, AI, and creating cool stuff. This is my first big project, and I'm using it to learn Python, Kivy, Git, and GitHub.

*   **My GitHub journey has just begun.** My repository might be a bit messy as I'm still learning best practices for commits, branches, and documentation. Thank you for your understanding!
*   **I welcome all help!** If you have suggestions on code, architecture, or how to use Git better, please let me know.

### 🚀 Running

Here's guide how to run ArtikGram

First, [get your own API credentials](my.telegram.org):

1. Log in to your Telegram account

2. Click on [API development tools](https://my.telegram.org/apps)

3. Create your app

4. Copy your API ID and API Hash

  ### Windows
  Install [python](https://www.python.org/downloads/windows/), [git](https://git-scm.com/downloads/win), [Microsoft Visual Studio C++](https://visualstudio.microsoft.com/ru/vs/community/) (Enable C++ support while installing), [CMake](https://cmake.org/download/) (choose "Add CMake to the system PATH" option while installing), [PHP](https://windows.php.net/download) (Add the path to php.exe to the PATH environment variable) and [build tdlib for windows](https://tdlib.github.io/td/build.html)

  You can use this command and instrutions or generate your own (recomended)
  
  Write this in powershell after installing required software
  ```
  git clone https://github.com/tdlib/td.git
cd td
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
git checkout bc3512a509f9d29b37346a7e7e929f9a26e66c7e
./bootstrap-vcpkg.bat
./vcpkg.exe install gperf:x64-windows openssl:x64-windows zlib:x64-windows
cd ..
Remove-Item build -Force -Recurse -ErrorAction SilentlyContinue
mkdir build
cd build
cmake -A x64 -DCMAKE_INSTALL_PREFIX:PATH=../tdlib -DCMAKE_TOOLCHAIN_FILE:FILEPATH=../vcpkg/scripts/buildsystems/vcpkg.cmake ..
cmake --build . --target install --config Release
cd ..
cd ..
dir td/tdlib
  ```
Then clone artikgram repository:
```
git clone https://github.com/artkruss777/ArtikGram
```
go to ArtikGram folder:

```
cd ArtikGram
```
Then activate venv (optional) and install requirements
```
python -m venv .venv
.venv/Scripts/activate
pip install -r requirments.txt
```

Create .env file (or edit config.py)

```
TG_API_ID= #Your API ID here
TG_API_HASH= #Your API HASH here
```

And finnaly run ArtikGram!
```
python main.py
```

  ### Linux
  First, install the required dependencies for your distribution.

  **Ubuntu/Debian**
  ```
  sudo apt update
sudo apt install git cmake g++ build-essential zlib1g-dev libssl-dev php curl python3 python3-pip python3-venv
  ```

  **Fedora**
  ```
  sudo dnf install git cmake gcc-c++ make zlib-devel openssl-devel php curl python3 python3-pip
  ```

  **Arch Linux**
  ```
  sudo pacman -S git cmake gcc zlib openssl php curl python python-pip
  ```

  **OpenSUSE**
  ```
  sudo zypper install git cmake gcc-c++ zlib-devel libopenssl-devel php curl python3 python3-pip
  ```

  Now build tdlib:

  You can use this command and instrutions or [generate your own](https://tdlib.github.io/td/build.html) (recomended)

  ```
    git clone https://github.com/tdlib/td.git
    cd td
    rm -rf build
    mkdir build
    cd build
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=../tdlib ..
    cmake --build . --target install
    cd ..
    cd ..
    ls -l td/tdlib
  ```
  Then clone artikgram repository:
```
git clone https://github.com/artkruss777/ArtikGram
```
go to ArtikGram folder:

```
cd ArtikGram
```
Then activate venv (optional) and install requirements
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirments.txt
```

Now create .env file.

```
touch .env
```

And edit it
```
nano .env
```
It should look like this
```
TG_API_ID= #Your API ID here
TG_API_HASH= #Your API HASH here
```

And finnaly run ArtikGram!
```
python main.py
```

  ### Android (May not work, beta version, not tested yet)

  [Download Termux](https://termux.dev/en/) on your phone.

  Give storage permission.

  ```
  termux-setup-storage
  ``` 

  Open termux.

  Install dependencies:
  ```

pkg update && pkg upgrade -y
pkg install python git cmake make clang openssl zlib libcrypt php
  ```

  Build tdlib.

  You can use this command and instrutions or [generate your own](https://tdlib.github.io/td/build.html) (recomended)

  ```
  git clone https://github.com/tdlib/td.git
cd td
rm -rf build
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=../tdlib ..
cmake --build . --target install
cd ..
cd ..
ls -l td/tdlib
  ```

    Then clone artikgram repository:
```
git clone https://github.com/artkruss777/ArtikGram
```
go to ArtikGram folder:

```
cd ArtikGram
```
Then activate venv (optional) and install requirements
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirments.txt
```
Now create .env file.

```
touch .env
```

And edit it
```
nano .env
```
It should look like this
```
TG_API_ID= #Your API ID here
TG_API_HASH= #Your API HASH here
```
And finnaly run ArtikGram!
```
python main.py
```
Create a configuration file for Kivy:

```
# Create .kivy directory if it doesn't exist
mkdir -p ~/.kivy

# Create config file
cat > ~/.kivy/config.ini << EOF
[graphics]
display = -1
width = auto
height = auto
maxfps = 60
multisamples = 2
show_cursor = 1
window_icon = 
resizable = 1
borderless = 0
fullscreen = auto
rotation = 0
position = auto
top = 0
left = 0
EOF
```
Troubleshooting
If you get "Cannot open display" error:
bash
```
# Install X11 support (if available)
pkg install x11-repo -y
pkg install tigervnc -y

# Or use Termux:X11 from F-Droid for better GUI support
```
If Kivy has rendering issues:
bash
```
# Try different Kivy backend
export KIVY_GL_BACKEND=sdl2
```

### 📬 Contact Me

Have a question, want to follow progress, or just say hi?
*   **Telegram:** [@artikruss777](https://t.me/artikruss777)
*   **Project Channel:** [t.me/artikgram](https://t.me/artikgram)
*   **Email:** [artembahanov156@gmail.com](mailto:artembahanov156@gmail.com)

---

> **Dream big, start small, and learn by doing.**