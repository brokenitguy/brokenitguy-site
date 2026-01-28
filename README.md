# 💀 BrokenITGuy | System Reboot

> **"System currently offline for critical maintenance."**

This is the personal landing page and technical portfolio for **BrokenITGuy**. The site is a living document of a "Hard Reset"—paralleling a journey of physical recovery from spinal fusion surgery with a professional career reboot in the IT industry.

The aesthetic merges **biological fragility** (X-rays, organic curves) with **digital rigidity** (Terminal lines, server racks, monospace fonts).

---

## 🎨 Design System & Theme

The UI mimics an old-school CRT terminal monitor sitting in a modern data center.

### 1. The Color Palette
Derived directly from the brand identity to maintain a high-contrast, late-night sysadmin vibe:

* **`#0d0d0d` (Void Black)**: The background canvas.
* **`#00d1b2` (Primary Teal)**: Represents the "System." Used for borders and prompts.
* **`#39ff14` (Success Green)**: Used for the live "System Uptime" ticker.
* **`#e0e0e0` (Text Cream)**: The "Human" element. Softer than pure white for readability.

### 2. Visual Layout
* **Background**: A composite image (`background.png`) merging a spinal fusion X-ray with a server rack data stream.
* **Transparency**: The terminal sidebar uses **65% opacity**, ensuring the "backbone" (the X-ray) is visible through the interface.
* **Responsiveness**: The layout automatically shifts to a full-width mobile view for accessibility on all devices.

---

## 🏗️ Technical Architecture

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5 / CSS3 | Static, lightweight terminal-style interface. |
| **Hosting** | Netlify / GitHub | Automated deployment from the main repository. |
| **Interactivity** | Netlify Forms | Backend-less suggestion box handling. |
| **Automation** | Python 3 | Custom script (`update.py`) to parse unformatted notes into JSON. |

---

## 🚀 Key Features & Automation

### 1. Descriptive System Uptime
The site features a live JavaScript ticker hardcoded to start from the domain purchase on **March 19, 2024**. It calculates and displays time in a human-readable **"X Days, Y Hours, Z Mins"** format to quantify the resilience of the reboot.

### 2. Suggestion Feed [Packet Transmission]
A fixed widget in the lower-right corner allows for direct feedback. It uses `data-netlify="true"` to capture messages without a database and is configured to trigger email notifications to `brokenitguy@proton.me`.

### 3. Root-Relative Navigation
To solve pathing errors between local VS Code environments and live production, all navigation uses relative paths (e.g., `href="log.html"`). This ensures CSS and background images remain stable during navigation.

---

## 🛠️ Maintenance Routine

To update the site or push new logs, execute the following in the project terminal:

```bash
# Stage the changes
git add .

# Save the version with a note
git commit -m "Update system logs"

# Push to live production
git push