<p align="center">
  <h1 align="center">💻 botyaradash</h1>
  <p align="center">
    <em>A powerful, cross-platform system monitoring dashboard built with Python & Rich</em>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-green?style=flat-square" alt="Platform">
    <img src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square" alt="License">
  </p>
</p>

---

## ✨ Features

| Category | Details |
|----------|---------|
| 🧠 **CPU** | Overall + per-core usage, frequency, temperature |
| 🐏 **Memory** | RAM & Swap with cached/buffers breakdown |
| 💾 **Disks** | All mount points, auto-detect NVMe / SSD / HDD, I/O speeds |
| 🌐 **Network** | Per-interface traffic, IP addresses, upload/download speeds |
| 🎮 **GPU** | NVIDIA GPU load, VRAM, temperature (via GPUtil) |
| 🔋 **Battery** | Charge level, status, time remaining (laptops) |
| ⚡ **Processes** | Top processes by CPU & memory usage |
| 📊 **Sparklines** | Real-time mini-graphs for CPU, RAM, network |
| 🎨 **10 Themes** | Dracula, Nord, Catppuccin, Cyberpunk & more |
| 🌍 **i18n** | English & Russian, switchable on the fly |
| ⌨️ **Hotkeys** | Full keyboard navigation with tabs |
| 📁 **Export** | Snapshot to JSON or CSV |
| 🔔 **Alerts** | Configurable thresholds for CPU, RAM, disk, temp |
| ⚙️ **Config** | Persistent TOML config in `~/.config/botyaradash/` |

---

## 📸 Preview

```
┌──────────────────────────────────────────────────────────────────────┐
│ 💻 botyaradash | 2025-01-15 14:32:07 | 🎨 Dracula | 🌐 EN         │
├──────────────────────────────────────────────────────────────────────┤
│ 【1:Overview】   2:CPU & Memory   3:Disks   4:Network   5:Processes │
│                                                                      │
│ 📊 Overview                                                          │
│ ┌────┬──────────────┬──────────────────────┬────────┬──────────────┐ │
│ │    │ Resource     │ Usage                │ Pct    │ History      │ │
│ ├────┼──────────────┼──────────────────────┼────────┼──────────────┤ │
│ │ 🟢 │ CPU          │ ████████░░░░ 67%     │  67%   │ ▁▂▃▅▇█▅▃▂▁  │ │
│ │ 🟡 │ RAM          │ ██████████░░ 82%     │  82%   │ ▃▃▄▅▅▆▆▇▇█  │ │
│ │ 🟢 │ Disk [/] SSD │ ██████░░░░░░ 45%     │  45%   │              │ │
│ │ 🌐 │ Network      │ ↑ 1.23 MB/s ↓ 5.67  │        │ ▁▁▂▃▅▃▂▁▁▂  │ │
│ └────┴──────────────┴──────────────────────┴────────┴──────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python **3.10+**
- pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/botyaradash.git
cd botyaradash

# Install dependencies
pip install -r requirements.txt

# Run!
python main.py
```

### Optional: GPU Monitoring

For NVIDIA GPU stats, make sure you have the NVIDIA drivers installed.
GPUtil will be used automatically if a compatible GPU is detected.

---

## 🎮 Usage

### Basic

```bash
python main.py
```

### CLI Options

```bash
python main.py [OPTIONS]
```

| Option | Description | Example |
|--------|-------------|---------|
| `--theme` | Choose a color theme | `--theme dracula` |
| `--lang` | Set language (`en` / `ru`) | `--lang ru` |
| `--layout` | Layout mode (`full` / `compact` / `minimal`) | `--layout compact` |
| `--refresh` | Refresh rate in seconds | `--refresh 1.0` |
| `--export` | Auto-export format | `--export json` |
| `--export-interval` | Auto-export interval (sec) | `--export-interval 30` |
| `--no-gpu` | Disable GPU monitoring | `--no-gpu` |
| `--processes` | Number of top processes | `--processes 10` |
| `--bar-width` | Progress bar width | `--bar-width 30` |
| `--save-config` | Save options as default | `--save-config` |
| `--help` | Show help | `--help` |

### Examples

```bash
# Cyberpunk theme in Russian
python main.py --theme cyberpunk --lang ru

# Compact layout, export every 60s
python main.py --layout compact --export csv --export-interval 60

# Save your preferences permanently
python main.py --theme nord --lang en --save-config
```

---

## ⌨️ Hotkeys

| Key | Action |
|-----|--------|
| `q` | 🚪 Quit |
| `t` | 🎨 Next theme |
| `T` | 🎨 Previous theme |
| `l` | 📐 Next layout |
| `L` | 🌍 Switch language |
| `e` | 📁 Export snapshot |
| `a` | 🔔 Toggle alerts |
| `h` / `?` | ❓ Toggle help overlay |
| `c` | 🧠 Toggle per-core CPU |
| `1` – `5` | 🔢 Switch to tab |
| `←` `→` | ⬅️➡️ Navigate tabs |
| `Tab` | ➡️ Next tab |

---

## 🎨 Themes

| # | Theme | Vibe |
|---|-------|------|
| 1 | `default` | 🟢 Clean & classic |
| 2 | `dracula` | 🧛 Dark purple |
| 3 | `monokai` | 🎨 Vibrant contrast |
| 4 | `nord` | ❄️ Cool arctic |
| 5 | `gruvbox` | 🟤 Warm retro |
| 6 | `solarized` | ☀️ Balanced tones |
| 7 | `catppuccin` | 🐱 Soft pastel |
| 8 | `tokyo_night` | 🌃 Neon city |
| 9 | `one_dark` | 🌑 Sleek dark |
| 10 | `cyberpunk` | 💜 Neon glow |

---

## ⚙️ Configuration

Config is automatically saved to your system's standard config directory:

| OS | Path |
|----|------|
| 🐧 Linux | `~/.config/botyaradash/config.toml` |
| 🍎 macOS | `~/Library/Application Support/botyaradash/config.toml` |
| 🪟 Windows | `%APPDATA%\botyaradash\config.toml` |

### Example `config.toml`

```toml
theme = "dracula"
language = "en"
layout = "full"
refresh_rate = 2.0
bar_width = 20
warn_percent = 60
crit_percent = 85
alerts_enabled = true
alert_cpu_threshold = 90
alert_ram_threshold = 90
alert_disk_threshold = 95
alert_temp_threshold = 85
export_format = "json"
export_interval = 60
history_length = 60
show_gpu = true
show_battery = true
show_processes = true
process_count = 8
sparkline_width = 20
```

---

## 📂 Project Structure

```
botyaradash/
├── main.py              # 🚀 Entry point
├── app.py               # 🏗️  Main application loop
├── cli.py               # 🖥️  CLI argument parsing
├── config.py            # ⚙️  Configuration management
├── i18n.py              # 🌍 Internationalization
├── history.py           # 📈 Value history for sparklines
├── alerts.py            # 🔔 Alert system
├── export.py            # 📁 JSON/CSV export
├── hotkeys.py           # ⌨️  Cross-platform key input
├── platform_utils.py    # 🖥️  OS-specific utilities
├── collectors/          # 📊 Data collectors
│   ├── cpu.py           #   🧠 CPU stats
│   ├── memory.py        #   🐏 RAM & Swap
│   ├── disk.py          #   💾 Disk usage & I/O
│   ├── network.py       #   🌐 Network interfaces
│   ├── gpu.py           #   🎮 GPU stats
│   ├── battery.py       #   🔋 Battery info
│   ├── process.py       #   ⚡ Top processes
│   └── system.py        #   🖥️  System info
├── ui/                  # 🎨 Rendering
│   ├── dashboard.py     #   📊 Dashboard renderer
│   ├── widgets.py       #   🧩 Bars, sparklines, icons
│   ├── themes.py        #   🎨 10 color themes
│   └── layouts.py       #   📐 Layout modes
├── requirements.txt     # 📦 Dependencies
├── .gitignore           # 🙈 Git ignore rules
└── README.md            # 📖 You are here!
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `psutil` | System & process monitoring |
| `rich` | Terminal UI rendering |
| `click` | CLI argument parsing |
| `GPUtil` | NVIDIA GPU monitoring |
| `toml` | Config file parsing |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repo
2. 🌿 Create a feature branch
3. ✏️ Make your changes
4. 🧪 Test on Linux / macOS / Windows
5. 📬 Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ and too much coffee ☕
</p>
