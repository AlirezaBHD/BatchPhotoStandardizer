# 📸 Automated Image Processor for Welfare Organization

<img width="1438" height="1018" alt="landing" src="https://github.com/user-attachments/assets/89fbe9d6-354e-4ea4-9e86-eec421c0ccd2" />



This is a **portable Windows application** that automates the process of standardizing personnel image files used by the **Welfare Organization**.

## 🚀 Project Purpose

The WO uses attendance control devices that store personnel images with the format: LF + 11-digit code + .png


Manually processing and renaming these images is time-consuming and error-prone. This application was developed to fully **automate** the following tasks:

- ✅ Remove the `LF` prefix
- ✅ Replace the 11-digit identification code with the **employee's card number**
- ✅ Convert image files from `.png` to `.jpg`

---

## 🔧 How It Works

1. The user provides an **Excel file** containing:
   - 11-digit identification codes
   - Employee card numbers

2. The program reads all `.png` images from the selected folder.

3. For each image:
   - It finds the matching card number.
   - Renames the image using that card number.
   - Converts it to `.jpg`.

4. A report Excel file is generated listing:
   - Images with no matching card number
   - Card numbers with no corresponding image

---

## 💡 Features

- ✅ Fully portable `.exe` (no installation required)
- ✅ Excel input support
- ✅ Duplicate checking (images already processed are skipped)
- ✅ Generates report for incomplete/missing data
- ✅ Saves time and reduces human error

---

## 🧪 Testing

Dummy image files and Excel samples are included in the release for testing purposes.  
Feel free to test the program with these samples before using your real data.
