# ⚡ Vamp OSINT Collector v3.0 - Quick Start

🚀 **Advanced OSINT Tool with Modern GUI Interface**

## 🎯 **What This Tool Does**

✅ **Social Media Investigation** - Search usernames across 15+ platforms  
✅ **Domain Analysis** - DNS, WHOIS, technology detection  
✅ **IP Intelligence** - Geolocation, port scanning, network info  
✅ **Email Investigation** - Security assessment, MX records  
✅ **Modern GUI** - Dark theme, real-time progress, export capabilities  

## 🚀 **Quick Installation**

### **Requirements**
- Python 3.7+ 
- Internet connection
- 4GB RAM (8GB recommended)

### **Install & Run**
```bash
# 1. Create folder and download files
mkdir vamp-osint-gui && cd vamp-osint-gui

# 2. Install dependencies  
pip install requests dnspython python-whois Pillow colorama

# 3. Run the application
python vamp_osint_gui.py
```

### **Automated Setup**
```bash
# Run setup script for automatic installation
python setup.py
```

## 🎮 **How to Use**

### **Step 1: Launch Application**
- Run `python vamp_osint_gui.py`
- Modern GUI interface will open

### **Step 2: Configure Targets**
Enter one or more targets in the Collection tab:
- **👤 Username** - Social media investigation
- **🌐 Domain** - Website analysis (e.g., example.com)
- **📍 IP Address** - Network investigation (e.g., 8.8.8.8)
- **📧 Email** - Security assessment (e.g., user@domain.com)

### **Step 3: Adjust Settings**
- **🔄 Threads**: 1-20 (10 recommended)
- **⏱️ Timeout**: 5-60 seconds (10 recommended)
- **🔬 Deep Scan**: Enable for comprehensive analysis

### **Step 4: Start Collection**
- Click **🚀 Start Collection**
- Watch real-time progress in output panel
- Results appear in the Results tab

### **Step 5: Export Results**
- Click **📊 Export Report** to save JSON file
- Double-click results for detailed view

## 📋 **Example Investigations**

### **🕵️ Person Investigation**
```
Username: john_doe
→ Finds: GitHub, Twitter, LinkedIn profiles
→ Result: Social media presence mapped
```

### **🏢 Company Investigation**  
```
Domain: company.com
→ Finds: DNS records, technologies, WHOIS data
→ Result: Infrastructure analysis complete
```

### **🌐 IP Investigation**
```
IP: 8.8.8.8  
→ Finds: Google LLC, Mountain View CA, open ports
→ Result: Network intelligence gathered
```

### **📧 Email Investigation**
```
Email: contact@domain.com
→ Finds: MX records, SPF/DMARC status
→ Result: Email security assessed
```

## 🎨 **GUI Features**

### **🔍 Collection Tab**
- **Target Input Fields** - Username, domain, IP, email
- **Live Output Console** - Real-time collection progress  
- **Progress Bar** - Visual completion indicator
- **Control Buttons** - Start/stop collection

### **📊 Results Tab**
- **Results Tree** - Organized data display
- **Sortable Columns** - Click headers to sort
- **Detail View** - Double-click for JSON data
- **Export Function** - Save reports

### **⚙️ Settings Tab**
- **API Keys** - Optional integrations
- **Performance Options** - Threading, timeouts
- **About Information** - Tool details

## 🔧 **Advanced Configuration**

### **🚀 Performance Tuning**
```
Fast Network: 15-20 threads, 5-8s timeout
Normal Network: 8-12 threads, 10-15s timeout  
Slow Network: 3-5 threads, 20-30s timeout
```

### **🎯 Investigation Strategies**
```
Individual: Username → Domain → Email → IP
Organization: Domain → Email → IP → Username
Security: Deep Scan enabled, all targets
```

## 📊 **Sample Output**

### **Username Results**
```
✅ Found on GitHub: https://github.com/john_doe
✅ Found on Twitter: https://twitter.com/john_doe  
❌ Not found on Instagram
📊 Summary: Found 2 profiles out of 15 platforms
```

### **Domain Results**
