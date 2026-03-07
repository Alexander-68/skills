Here is the simplified guide to checking and using GPU acceleration with FFmpeg, broken down by task and operating system.

---

## **1\. Check if FFmpeg Supports Hardware Encoding**

Before checking your hardware, you need to see if your version of FFmpeg includes the necessary "hooks" for GPUs.

**On Windows (PowerShell):** Run: `ffmpeg -encoders | Select-String "nvenc|qsv|amf|vaapi|videotoolbox"`

**On Linux or macOS (Terminal):** Run: `ffmpeg -encoders | grep -E "nvenc|qsv|amf|vaapi|videotoolbox"`

**What to look for in the results:**

* **nvenc**: Support for NVIDIA GPUs.  
* **qsv**: Support for Intel Quick Sync Video.  
* **amf**: Support for AMD GPUs (Windows).  
* **vaapi**: Support for Intel/AMD (Linux).  
* **videotoolbox**: Support for Apple Silicon and modern Macs.

---

## **2\. Identify Your Physical Hardware**

You need to confirm what GPU is actually inside your machine to know which encoder to use.

**Windows:** Run this in PowerShell: `Get-CimInstance Win32_VideoController | Select-Object Name`

* Look for "NVIDIA", "Intel Iris", or "AMD Radeon".

**Linux:** Run this in Terminal: `lspci | grep -i vga`

* This will list the manufacturer of your video card.

**macOS:** Click the Apple Menu \> About This Mac, or run in Terminal: `system_profiler SPDisplaysDataType`

* Look for "Chip" (e.g., Apple M2) or "Video Card".

---

## **3\. Match Your Hardware to the Right Encoder**

Once you know your hardware, use these specific names in your FFmpeg commands (typically after the `-c:v` flag).

**NVIDIA GPUs (Windows & Linux):** Use **h264\_nvenc** for H.264 video or **hevc\_nvenc** for H.265.

**Intel GPUs (Windows & Linux):** Use **h264\_qsv** or **hevc\_qsv**. (Note: On Linux, you may also use **h264\_vaapi**).

**AMD GPUs:**

* On **Windows**: Use **h264\_amf** or **hevc\_amf**.  
* On **Linux**: Use **h264\_vaapi** or **hevc\_vaapi**.

**Apple Silicon / Macs:** Use **h264\_videotoolbox** or **hevc\_videotoolbox**.

---

## **4\. How to Test Your GPU Connection**

The best way to verify everything is working is to run a "Null Test." This simulates an encoding process without creating a file, purely to see if the GPU responds.

**Test NVIDIA:** `ffmpeg -f lavfi -i testsrc -c:v h264_nvenc -f null -`

**Test Intel (QSV):** `ffmpeg -f lavfi -i testsrc -c:v h264_qsv -f null -`

**Test AMD (Windows):** `ffmpeg -f lavfi -i testsrc -c:v h264_amf -f null -`

**Test Apple (Mac):** `ffmpeg -f lavfi -i testsrc -c:v h264_videotoolbox -f null -`

**If it works:** You will see frame numbers counting up rapidly. **If it fails:** You will see an error like "Device not found" or "Function not implemented," which usually means you need to update your graphics drivers.

