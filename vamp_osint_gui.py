#!/usr/bin/env python3
"""
Vamp OSINT Collector v3.0 - GUI Edition
Advanced OSINT Collection Tool with Modern GUI
Author: Vamp Security Channel
License: MIT

Usage: python vamp_osint_gui.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
import socket
import json
import time
import os
import sys
import threading
from datetime import datetime
from urllib.parse import urlparse
import dns.resolver
import whois
import concurrent.futures
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import re
import urllib3
import subprocess
import webbrowser
from PIL import Image, ImageTk
import io
import base64

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@dataclass
class OSINTResult:
    """Data class for OSINT collection results"""
    source: str
    data_type: str
    timestamp: str
    data: Dict[str, Any]
    status: str

class ModernOSINTCollector:
    """Advanced OSINT Collection Tool with GUI"""
    
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 10
        self.max_threads = 10
        self.is_running = False
        
        # Enhanced social media platforms
        self.social_platforms = {
            'github': {
                'url': 'https://github.com/{}',
                'name': 'GitHub',
                'icon': '👨‍💻'
            },
            'twitter': {
                'url': 'https://twitter.com/{}',
                'name': 'Twitter/X',
                'icon': '🐦'
            },
            'instagram': {
                'url': 'https://instagram.com/{}',
                'name': 'Instagram',
                'icon': '📷'
            },
            'linkedin': {
                'url': 'https://linkedin.com/in/{}',
                'name': 'LinkedIn',
                'icon': '💼'
            },
            'reddit': {
                'url': 'https://reddit.com/user/{}',
                'name': 'Reddit',
                'icon': '🤖'
            },
            'pinterest': {
                'url': 'https://pinterest.com/{}',
                'name': 'Pinterest',
                'icon': '📌'
            },
            'youtube': {
                'url': 'https://youtube.com/@{}',
                'name': 'YouTube',
                'icon': '📺'
            },
            'tiktok': {
                'url': 'https://tiktok.com/@{}',
                'name': 'TikTok',
                'icon': '🎵'
            },
            'facebook': {
                'url': 'https://facebook.com/{}',
                'name': 'Facebook',
                'icon': '👥'
            },
            'telegram': {
                'url': 'https://t.me/{}',
                'name': 'Telegram',
                'icon': '✈️'
            },
            'discord': {
                'url': 'https://discord.com/users/{}',
                'name': 'Discord',
                'icon': '🎮'
            },
            'twitch': {
                'url': 'https://twitch.tv/{}',
                'name': 'Twitch',
                'icon': '🎮'
            },
            'medium': {
                'url': 'https://medium.com/@{}',
                'name': 'Medium',
                'icon': '📝'
            },
            'behance': {
                'url': 'https://behance.net/{}',
                'name': 'Behance',
                'icon': '🎨'
            },
            'dribbble': {
                'url': 'https://dribbble.com/{}',
                'name': 'Dribbble',
                'icon': '🏀'
            }
        }

    def setup_gui(self):
        """Setup the modern GUI interface"""
        self.root = tk.Tk()
        self.root.title("Vamp OSINT Collector v3.0 - Advanced Intelligence Tool")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_tertiary': '#0f3460',
            'accent': '#10b981',
            'accent_hover': '#059669',
            'text_primary': '#ffffff',
            'text_secondary': '#cbd5e1',
            'text_muted': '#94a3b8',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'success': '#10b981'
        }
        
        # Configure styles
        self.setup_styles()
        
        # Configure root
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Create main layout
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        return self.root

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure(
            'Modern.TNotebook',
            background=self.colors['bg_secondary'],
            borderwidth=0,
            tabmargins=[2, 5, 2, 0]
        )
        
        style.configure(
            'Modern.TNotebook.Tab',
            background=self.colors['bg_tertiary'],
            foreground=self.colors['text_secondary'],
            padding=[20, 10],
            borderwidth=0,
            focuscolor='none'
        )
        
        style.map(
            'Modern.TNotebook.Tab',
            background=[('selected', self.colors['accent'])],
            foreground=[('selected', self.colors['text_primary'])]
        )
        
        # Configure button styles
        style.configure(
            'Accent.TButton',
            background=self.colors['accent'],
            foreground=self.colors['text_primary'],
            borderwidth=0,
            focuscolor='none',
            padding=[20, 10]
        )
        
        style.map(
            'Accent.TButton',
            background=[('active', self.colors['accent_hover'])]
        )
        
        # Configure entry styles
        style.configure(
            'Modern.TEntry',
            fieldbackground=self.colors['bg_tertiary'],
            foreground=self.colors['text_primary'],
            borderwidth=1,
            insertcolor=self.colors['text_primary']
        )
        
        # Configure frame styles
        style.configure(
            'Modern.TFrame',
            background=self.colors['bg_secondary'],
            borderwidth=0
        )

    def create_header(self):
        """Create modern header with branding"""
        header_frame = tk.Frame(
            self.root,
            bg=self.colors['bg_secondary'],
            height=80
        )
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        title_frame.pack(side='left', padx=20, pady=15)
        
        # Title with icon
        title_label = tk.Label(
            title_frame,
            text="⚡ Vamp OSINT Collector v3.0",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(
            title_frame,
            text="Advanced Open Source Intelligence Tool",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        subtitle_label.pack(side='left', padx=(20, 0))
        
        # Action buttons
        buttons_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        buttons_frame.pack(side='right', padx=20, pady=15)
        
        self.export_btn = tk.Button(
            buttons_frame,
            text="📊 Export Report",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            border=0,
            padx=15,
            pady=8,
            command=self.export_report,
            cursor='hand2'
        )
        self.export_btn.pack(side='right', padx=(10, 0))
        
        self.clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ Clear All",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['warning'],
            fg=self.colors['text_primary'],
            border=0,
            padx=15,
            pady=8,
            command=self.clear_all_results,
            cursor='hand2'
        )
        self.clear_btn.pack(side='right', padx=(10, 0))

    def create_main_content(self):
        """Create main content area with tabs"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_collection_tab()
        self.create_results_tab()
        self.create_settings_tab()

    def create_collection_tab(self):
        """Create the main collection interface"""
        # Collection tab frame
        collection_frame = tk.Frame(self.notebook, bg=self.colors['bg_secondary'])
        self.notebook.add(collection_frame, text='🔍 Collection')
        
        # Left panel - Input controls
        left_panel = tk.Frame(collection_frame, bg=self.colors['bg_secondary'], width=400)
        left_panel.pack(side='left', fill='y', padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        # Input section
        self.create_input_section(left_panel)
        
        # Right panel - Live output
        right_panel = tk.Frame(collection_frame, bg=self.colors['bg_secondary'])
        right_panel.pack(side='right', fill='both', expand=True, padx=(0, 10), pady=10)
        
        self.create_output_section(right_panel)

    def create_input_section(self, parent):
        """Create input controls section"""
        # Title
        title_label = tk.Label(
            parent,
            text="🎯 Target Configuration",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Username input
        self.create_input_field(parent, "👤 Username", "username_var", "Enter username to investigate")
        
        # Domain input
        self.create_input_field(parent, "🌐 Domain", "domain_var", "Enter domain (e.g., example.com)")
        
        # IP input
        self.create_input_field(parent, "📍 IP Address", "ip_var", "Enter IP address (e.g., 8.8.8.8)")
        
        # Email input
        self.create_input_field(parent, "📧 Email", "email_var", "Enter email address")
        
        # Collection options
        options_frame = tk.LabelFrame(
            parent,
            text="⚙️ Collection Options",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            bd=1,
            relief='solid'
        )
        options_frame.pack(fill='x', pady=(20, 0))
        
        # Threading option
        threads_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'])
        threads_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            threads_frame,
            text="🔄 Threads:",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left')
        
        self.threads_var = tk.IntVar(value=10)
        threads_spinbox = tk.Spinbox(
            threads_frame,
            from_=1,
            to=20,
            textvariable=self.threads_var,
            width=5,
            font=('Segoe UI', 10),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            border=1
        )
        threads_spinbox.pack(side='right')
        
        # Timeout option
        timeout_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'])
        timeout_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            timeout_frame,
            text="⏱️ Timeout (s):",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left')
        
        self.timeout_var = tk.IntVar(value=10)
        timeout_spinbox = tk.Spinbox(
            timeout_frame,
            from_=5,
            to=60,
            textvariable=self.timeout_var,
            width=5,
            font=('Segoe UI', 10),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            border=1
        )
        timeout_spinbox.pack(side='right')
        
        # Deep scan option
        self.deep_scan_var = tk.BooleanVar(value=False)
        deep_scan_cb = tk.Checkbutton(
            options_frame,
            text="🔬 Deep Scan (slower but more thorough)",
            variable=self.deep_scan_var,
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_tertiary'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        )
        deep_scan_cb.pack(anchor='w', padx=10, pady=5)
        
        # Control buttons
        buttons_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        buttons_frame.pack(fill='x', pady=(30, 0))
        
        # Start collection button
        self.start_btn = tk.Button(
            buttons_frame,
            text="🚀 Start Collection",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['text_primary'],
            border=0,
            padx=20,
            pady=12,
            command=self.start_collection,
            cursor='hand2'
        )
        self.start_btn.pack(fill='x', pady=(0, 10))
        
        # Stop button
        self.stop_btn = tk.Button(
            buttons_frame,
            text="⏹️ Stop Collection",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['danger'],
            fg=self.colors['text_primary'],
            border=0,
            padx=20,
            pady=12,
            command=self.stop_collection,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(fill='x')

    def create_input_field(self, parent, label, var_name, placeholder):
        """Create a styled input field"""
        field_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        field_frame.pack(fill='x', pady=(0, 15))
        
        # Label
        label_widget = tk.Label(
            field_frame,
            text=label,
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        label_widget.pack(anchor='w', pady=(0, 5))
        
        # Entry
        var = tk.StringVar()
        setattr(self, var_name, var)
        
        entry = tk.Entry(
            field_frame,
            textvariable=var,
            font=('Segoe UI', 11),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            border=1,
            relief='solid',
            insertbackground=self.colors['text_primary']
        )
        entry.pack(fill='x', ipady=8)
        
        # Placeholder effect
        entry.insert(0, placeholder)
        entry.configure(fg=self.colors['text_muted'])
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(fg=self.colors['text_primary'])
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(fg=self.colors['text_muted'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def create_output_section(self, parent):
        """Create live output section"""
        # Title
        title_label = tk.Label(
            parent,
            text="📡 Live Collection Output",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Progress frame
        progress_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        progress_frame.pack(fill='x', pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(side='left', fill='x', expand=True)
        
        # Progress label
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        self.progress_label.pack(side='right', padx=(10, 0))
        
        # Output text area
        output_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        output_frame.pack(fill='both', expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            font=('Consolas', 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            border=1,
            relief='solid',
            wrap='word'
        )
        self.output_text.pack(fill='both', expand=True)
        
        # Configure text tags for colored output
        self.output_text.tag_configure('success', foreground=self.colors['success'])
        self.output_text.tag_configure('error', foreground=self.colors['danger'])
        self.output_text.tag_configure('warning', foreground=self.colors['warning'])
        self.output_text.tag_configure('info', foreground=self.colors['accent'])

    def create_results_tab(self):
        """Create results visualization tab"""
        results_frame = tk.Frame(self.notebook, bg=self.colors['bg_secondary'])
        self.notebook.add(results_frame, text='📊 Results')
        
        # Results tree
        tree_frame = tk.Frame(results_frame, bg=self.colors['bg_secondary'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            tree_frame,
            text="📋 Collection Results",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Create treeview
        columns = ('Source', 'Type', 'Status', 'Timestamp', 'Details')
        self.results_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=20
        )
        
        # Configure columns
        self.results_tree.heading('Source', text='Source')
        self.results_tree.heading('Type', text='Data Type')
        self.results_tree.heading('Status', text='Status')
        self.results_tree.heading('Timestamp', text='Timestamp')
        self.results_tree.heading('Details', text='Details')
        
        self.results_tree.column('Source', width=150)
        self.results_tree.column('Type', width=150)
        self.results_tree.column('Status', width=100)
        self.results_tree.column('Timestamp', width=150)
        self.results_tree.column('Details', width=300)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.results_tree.xview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack components
        self.results_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click
        self.results_tree.bind('<Double-1>', self.show_result_details)

    def create_settings_tab(self):
        """Create settings and configuration tab"""
        settings_frame = tk.Frame(self.notebook, bg=self.colors['bg_secondary'])
        self.notebook.add(settings_frame, text='⚙️ Settings')
        
        # Settings content
        content_frame = tk.Frame(settings_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text="⚙️ Application Settings",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(anchor='w', pady=(0, 30))
        
        # API Keys section
        api_frame = tk.LabelFrame(
            content_frame,
            text="🔑 API Keys (Optional)",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            bd=1,
            relief='solid'
        )
        api_frame.pack(fill='x', pady=(0, 20))
        
        # VirusTotal API
        vt_frame = tk.Frame(api_frame, bg=self.colors['bg_secondary'])
        vt_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            vt_frame,
            text="VirusTotal API Key:",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left')
        
        self.vt_api_var = tk.StringVar()
        vt_entry = tk.Entry(
            vt_frame,
            textvariable=self.vt_api_var,
            font=('Segoe UI', 10),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            show='*',
            width=40
        )
        vt_entry.pack(side='right', padx=(10, 0))
        
        # User Agents section
        ua_frame = tk.LabelFrame(
            content_frame,
            text="🕵️ User Agent Rotation",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            bd=1,
            relief='solid'
        )
        ua_frame.pack(fill='x', pady=(0, 20))
        
        self.rotate_ua_var = tk.BooleanVar(value=True)
        ua_cb = tk.Checkbutton(
            ua_frame,
            text="Enable User Agent Rotation",
            variable=self.rotate_ua_var,
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_tertiary']
        )
        ua_cb.pack(anchor='w', padx=10, pady=10)
        
        # About section
        about_frame = tk.LabelFrame(
            content_frame,
            text="ℹ️ About",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            bd=1,
            relief='solid'
        )
        about_frame.pack(fill='x')
        
        about_text = """
Vamp OSINT Collector v3.0
Advanced Open Source Intelligence Tool

Features:
• 15+ Social Media Platform Search
• Comprehensive Domain Analysis
• IP Geolocation & Port Scanning
• Email Security Assessment
• Real-time Progress Monitoring
• Modern GUI Interface
• Export Capabilities

Developed by Vamp Security Channel
        """
        
        about_label = tk.Label(
            about_frame,
            text=about_text,
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            justify='left'
        )
        about_label.pack(padx=10, pady=10)

    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(
            self.root,
            bg=self.colors['bg_tertiary'],
            height=30
        )
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready • Vamp OSINT Collector v3.0",
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_tertiary']
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Connection indicator
        self.connection_label = tk.Label(
            status_frame,
            text="🟢 Online",
            font=('Segoe UI', 9),
            fg=self.colors['success'],
            bg=self.colors['bg_tertiary']
        )
        self.connection_label.pack(side='right', padx=10, pady=5)

    def log_output(self, message, tag='info'):
        """Log message to output area"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        full_message = f"[{timestamp}] {message}\n"
        
        self.output_text.insert(tk.END, full_message, tag)
        self.output_text.see(tk.END)
        self.root.update_idletasks()

    def update_progress(self, value, text="Processing..."):
        """Update progress bar and label"""
        self.progress_var.set(value)
        self.progress_label.config(text=text)
        self.root.update_idletasks()

    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)

    def get_input_values(self):
        """Get all input values"""
        values = {}
        
        # Get values and check if they're not placeholders
        placeholders = {
            'username': "Enter username to investigate",
            'domain': "Enter domain (e.g., example.com)",
            'ip': "Enter IP address (e.g., 8.8.8.8)",
            'email': "Enter email address"
        }
        
        for key, placeholder in placeholders.items():
            var_name = f"{key}_var"
            if hasattr(self, var_name):
                value = getattr(self, var_name).get().strip()
                if value and value != placeholder:
                    values[key] = value
        
        return values

    def start_collection(self):
        """Start OSINT collection process"""
        if self.is_running:
            return
        
        # Get input values
        targets = self.get_input_values()
        
        if not targets:
            messagebox.showwarning(
                "No Targets",
                "Please enter at least one target (username, domain, IP, or email)."
            )
            return
        
        # Update settings
        self.max_threads = self.threads_var.get()
        self.timeout = self.timeout_var.get()
        
        # Clear previous results
        self.output_text.delete(1.0, tk.END)
        self.results.clear()
        
        # Update UI state
        self.is_running = True
        self.start_btn.config(state='disabled', text="🔄 Collecting...")
        self.stop_btn.config(state='normal')
        
        # Start collection in separate thread
        collection_thread = threading.Thread(
            target=self.run_collection,
            args=(targets,),
            daemon=True
        )
        collection_thread.start()

    def run_collection(self, targets):
        """Run the collection process"""
        try:
            self.log_output("🚀 Starting OSINT collection...", 'info')
            self.update_status("Collection in progress...")
            
            total_tasks = len(targets)
            completed_tasks = 0
            
            for target_type, target_value in targets.items():
                if not self.is_running:
                    break
                
                self.log_output(f"🎯 Processing {target_type}: {target_value}", 'info')
                
                try:
                    if target_type == 'username':
                        self.collect_username_info(target_value)
                    elif target_type == 'domain':
                        self.collect_domain_info(target_value)
                    elif target_type == 'ip':
                        self.collect_ip_info(target_value)
                    elif target_type == 'email':
                        self.collect_email_info(target_value)
                    
                    completed_tasks += 1
                    progress = (completed_tasks / total_tasks) * 100
                    self.update_progress(progress, f"Completed {completed_tasks}/{total_tasks}")
                    
                except Exception as e:
                    self.log_output(f"❌ Error processing {target_type}: {str(e)}", 'error')
            
            if self.is_running:
                self.log_output("✅ Collection completed successfully!", 'success')
                self.update_progress(100, "Completed")
                self.update_results_display()
            else:
                self.log_output("⚠️ Collection stopped by user", 'warning')
        
        except Exception as e:
            self.log_output(f"💥 Unexpected error: {str(e)}", 'error')
        
        finally:
            # Reset UI state
            self.is_running = False
            self.start_btn.config(state='normal', text="🚀 Start Collection")
            self.stop_btn.config(state='disabled')
            self.update_status("Ready")

    def stop_collection(self):
        """Stop the collection process"""
        self.is_running = False
        self.log_output("⏹️ Stopping collection...", 'warning')

    def collect_username_info(self, username):
        """Collect username information across social platforms"""
        self.log_output(f"👤 Searching username: {username}", 'info')
        
        found_platforms = []
        total_platforms = len(self.social_platforms)
        checked_platforms = 0
        
        def check_platform(platform_name, platform_info):
            nonlocal checked_platforms
            if not self.is_running:
                return
            
            url = platform_info['url'].format(username)
            
            try:
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
                
                # Check if profile exists
                if response.status_code == 200:
                    # Additional checks for some platforms
                    content = response.text.lower()
                    
                    # Platform-specific validation
                    is_valid = True
                    if platform_name == 'github' and 'not found' in content:
                        is_valid = False
                    elif platform_name == 'twitter' and 'suspended' in content:
                        is_valid = False
                    
                    if is_valid:
                        found_platforms.append({
                            'platform': platform_info['name'],
                            'url': url,
                            'icon': platform_info['icon'],
                            'status_code': response.status_code,
                            'found_at': datetime.now().isoformat()
                        })
                        self.log_output(f"  ✅ {platform_info['icon']} Found on {platform_info['name']}: {url}", 'success')
                    else:
                        self.log_output(f"  ❌ {platform_info['icon']} Not found on {platform_info['name']}", 'error')
                else:
                    self.log_output(f"  ❌ {platform_info['icon']} Not found on {platform_info['name']}", 'error')
            
            except Exception as e:
                self.log_output(f"  ⚠️ {platform_info['icon']} Error checking {platform_info['name']}: {str(e)}", 'warning')
            
            checked_platforms += 1
            progress = (checked_platforms / total_platforms) * 100
            self.update_progress(progress, f"Checking platforms... {checked_platforms}/{total_platforms}")
        
        # Use threading for faster collection
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [
                executor.submit(check_platform, platform_name, platform_info)
                for platform_name, platform_info in self.social_platforms.items()
            ]
            
            # Wait for completion or stop signal
            for future in concurrent.futures.as_completed(futures):
                if not self.is_running:
                    break
        
        # Log results
        result_data = {
            'username': username,
            'found_platforms': found_platforms,
            'total_found': len(found_platforms),
            'total_checked': total_platforms,
            'success_rate': f"{(len(found_platforms)/total_platforms)*100:.1f}%"
        }
        
        self.log_result("Username Search", "social_media", result_data)
        self.log_output(f"📊 Summary: Found {len(found_platforms)} profiles out of {total_platforms} platforms", 'info')

    def collect_domain_info(self, domain):
        """Collect comprehensive domain information"""
        self.log_output(f"🌐 Analyzing domain: {domain}", 'info')
        
        domain_data = {'domain': domain}
        
        try:
            # DNS Records
            self.log_output("  🔍 Collecting DNS records...", 'info')
            dns_records = {}
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
            
            for record_type in record_types:
                if not self.is_running:
                    return
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    dns_records[record_type] = [str(rdata) for rdata in answers]
                    self.log_output(f"    ✅ {record_type}: {len(dns_records[record_type])} records", 'success')
                except:
                    dns_records[record_type] = []
            
            domain_data['dns_records'] = dns_records
            
            # WHOIS Information
            self.log_output("  🔍 Collecting WHOIS information...", 'info')
            try:
                whois_info = whois.whois(domain)
                domain_data['whois'] = {
                    'registrar': str(whois_info.registrar) if whois_info.registrar else None,
                    'creation_date': str(whois_info.creation_date) if whois_info.creation_date else None,
                    'expiration_date': str(whois_info.expiration_date) if whois_info.expiration_date else None,
                    'updated_date': str(whois_info.updated_date) if whois_info.updated_date else None,
                    'name_servers': whois_info.name_servers if whois_info.name_servers else [],
                    'emails': whois_info.emails if whois_info.emails else []
                }
                self.log_output("    ✅ WHOIS data collected", 'success')
            except Exception as e:
                self.log_output(f"    ⚠️ WHOIS lookup failed: {str(e)}", 'warning')
            
            # HTTP Headers and Technology Detection
            self.log_output("  🔍 Analyzing web technologies...", 'info')
            for protocol in ['https', 'http']:
                if not self.is_running:
                    return
                try:
                    response = self.session.get(f"{protocol}://{domain}", timeout=self.timeout)
                    domain_data['http_info'] = {
                        'protocol': protocol,
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'technologies': self.detect_technologies(response.headers, response.text)
                    }
                    self.log_output(f"    ✅ Web analysis completed ({protocol.upper()})", 'success')
                    break
                except:
                    continue
            
            self.log_result("Domain Analysis", "domain_info", domain_data)
            
        except Exception as e:
            self.log_output(f"❌ Domain analysis failed: {str(e)}", 'error')

    def collect_ip_info(self, ip_address):
        """Collect IP address information"""
        self.log_output(f"📍 Analyzing IP: {ip_address}", 'info')
        
        ip_data = {'ip': ip_address}
        
        try:
            # Validate IP
            socket.inet_aton(ip_address)
            
            # Reverse DNS
            self.log_output("  🔍 Performing reverse DNS lookup...", 'info')
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                ip_data['hostname'] = hostname
                self.log_output(f"    ✅ Hostname: {hostname}", 'success')
            except:
                self.log_output("    ⚠️ Reverse DNS failed", 'warning')
            
            # Geolocation
            self.log_output("  🔍 Getting geolocation data...", 'info')
            geo_apis = [
                f"https://ipapi.co/{ip_address}/json/",
                f"http://ip-api.com/json/{ip_address}"
            ]
            
            for api_url in geo_apis:
                if not self.is_running:
                    return
                try:
                    response = self.session.get(api_url, timeout=self.timeout)
                    if response.status_code == 200:
                        geo_data = response.json()
                        
                        if 'ipapi.co' in api_url:
                            ip_data['geolocation'] = {
                                'country': geo_data.get('country_name'),
                                'city': geo_data.get('city'),
                                'region': geo_data.get('region'),
                                'isp': geo_data.get('org'),
                                'latitude': geo_data.get('latitude'),
                                'longitude': geo_data.get('longitude'),
                                'timezone': geo_data.get('timezone')
                            }
                        else:  # ip-api.com
                            ip_data['geolocation'] = {
                                'country': geo_data.get('country'),
                                'city': geo_data.get('city'),
                                'region': geo_data.get('regionName'),
                                'isp': geo_data.get('isp'),
                                'latitude': geo_data.get('lat'),
                                'longitude': geo_data.get('lon'),
                                'timezone': geo_data.get('timezone')
                            }
                        
                        self.log_output(f"    ✅ Location: {ip_data['geolocation'].get('city', 'Unknown')}, {ip_data['geolocation'].get('country', 'Unknown')}", 'success')
                        break
                except:
                    continue
            
            # Port scanning
            if self.deep_scan_var.get():
                self.log_output("  🔍 Scanning common ports...", 'info')
                common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5900, 8080]
                open_ports = []
                
                def scan_port(port):
                    if not self.is_running:
                        return
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((ip_address, port))
                    sock.close()
                    if result == 0:
                        open_ports.append(port)
                        self.log_output(f"    ✅ Port {port} is open", 'success')
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    executor.map(scan_port, common_ports)
                
                ip_data['open_ports'] = sorted(open_ports)
                self.log_output(f"    📊 Found {len(open_ports)} open ports", 'info')
            
            self.log_result("IP Analysis", "ip_info", ip_data)
            
        except Exception as e:
            self.log_output(f"❌ IP analysis failed: {str(e)}", 'error')

    def collect_email_info(self, email):
        """Collect email information"""
        self.log_output(f"📧 Analyzing email: {email}", 'info')
        
        email_data = {'email': email}
        
        try:
            # Validate email format
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                self.log_output("    ❌ Invalid email format", 'error')
                return
            
            domain = email.split('@')[1]
            email_data['domain'] = domain
            
            # Check MX records
            self.log_output("  🔍 Checking MX records...", 'info')
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                mx_records = [{'preference': rdata.preference, 'exchange': str(rdata.exchange)} for rdata in answers]
                email_data['mx_records'] = mx_records
                self.log_output(f"    ✅ Found {len(mx_records)} MX records", 'success')
            except:
                self.log_output("    ⚠️ No MX records found", 'warning')
                email_data['mx_records'] = []
            
            # Check SPF and DMARC records
            self.log_output("  🔍 Checking email security records...", 'info')
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                spf_records = []
                dmarc_records = []
                
                for rdata in txt_records:
                    txt_string = str(rdata)
                    if 'v=spf1' in txt_string:
                        spf_records.append(txt_string)
                    elif 'v=DMARC1' in txt_string:
                        dmarc_records.append(txt_string)
                
                # Check DMARC subdomain
                try:
                    dmarc_answers = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT')
                    for rdata in dmarc_answers:
                        dmarc_records.append(str(rdata))
                except:
                    pass
                
                email_data['security_records'] = {
                    'spf': spf_records,
                    'dmarc': dmarc_records
                }
                
                if spf_records:
                    self.log_output("    ✅ SPF records found", 'success')
                if dmarc_records:
                    self.log_output("    ✅ DMARC records found", 'success')
                    
            except:
                self.log_output("    ⚠️ No security records found", 'warning')
            
            self.log_result("Email Analysis", "email_info", email_data)
            
        except Exception as e:
            self.log_output(f"❌ Email analysis failed: {str(e)}", 'error')

    def detect_technologies(self, headers, content):
        """Detect web technologies from headers and content"""
        technologies = []
        
        # Server detection
        server = headers.get('Server', '').lower()
        if server:
            technologies.append({'type': 'Server', 'name': server})
        
        # Framework detection
        powered_by = headers.get('X-Powered-By', '')
        if powered_by:
            technologies.append({'type': 'Framework', 'name': powered_by})
        
        # CMS detection from content
        content_lower = content.lower()
        cms_signatures = {
            'wordpress': ['wp-content', 'wp-includes'],
            'drupal': ['drupal', 'sites/default'],
            'joomla': ['joomla', 'administrator'],
            'magento': ['magento', 'mage/']
        }
        
        for cms, signatures in cms_signatures.items():
            if any(sig in content_lower for sig in signatures):
                technologies.append({'type': 'CMS', 'name': cms.title()})
        
        return technologies

    def log_result(self, source, data_type, data, status="success"):
        """Log a collection result"""
        result = OSINTResult(
            source=source,
            data_type=data_type,
            timestamp=datetime.now().isoformat(),
            data=data,
            status=status
        )
        self.results.append(result)

    def update_results_display(self):
        """Update the results tree view"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add results
        for result in self.results:
            # Create summary of data
            summary = ""
            if result.data_type == "social_media":
                summary = f"Found on {result.data['total_found']} platforms"
            elif result.data_type == "domain_info":
                summary = f"Domain: {result.data['domain']}"
            elif result.data_type == "ip_info":
                location = result.data.get('geolocation', {})
                summary = f"Location: {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}"
            elif result.data_type == "email_info":
                mx_count = len(result.data.get('mx_records', []))
                summary = f"MX Records: {mx_count}"
            
            self.results_tree.insert(
                '',
                'end',
                values=(
                    result.source,
                    result.data_type,
                    result.status.title(),
                    result.timestamp.split('T')[1][:8],  # Time only
                    summary
                )
            )

    def show_result_details(self, event):
        """Show detailed result information"""
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = self.results_tree.item(selection[0])
        values = item['values']
        
        # Find the corresponding result
        result = None
        for r in self.results:
            if (r.source == values[0] and 
                r.data_type == values[1] and 
                r.timestamp.split('T')[1][:8] == values[3]):
                result = r
                break
        
        if result:
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Details - {result.source}")
            details_window.geometry("800x600")
            details_window.configure(bg=self.colors['bg_secondary'])
            
            # JSON display
            text_area = scrolledtext.ScrolledText(
                details_window,
                font=('Consolas', 10),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary'],
                wrap='word'
            )
            text_area.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Pretty print JSON
            json_text = json.dumps(result.data, indent=2, ensure_ascii=False, default=str)
            text_area.insert('1.0', json_text)

    def export_report(self):
        """Export results to JSON file"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export OSINT Report"
        )
        
        if filename:
            try:
                report_data = {
                    'report_metadata': {
                        'tool': 'Vamp OSINT Collector v3.0',
                        'generated_at': datetime.now().isoformat(),
                        'total_results': len(self.results)
                    },
                    'results': [
                        {
                            'source': result.source,
                            'data_type': result.data_type,
                            'timestamp': result.timestamp,
                            'status': result.status,
                            'data': result.data
                        }
                        for result in self.results
                    ]
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
                
                messagebox.showinfo("Export Successful", f"Report exported to:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Export Failed", f"Failed to export report:\n{str(e)}")

    def clear_all_results(self):
        """Clear all results and output"""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all results?"):
            self.results.clear()
            self.output_text.delete(1.0, tk.END)
            self.update_results_display()
            self.progress_var.set(0)
            self.progress_label.config(text="Ready")
            self.log_output("🗑️ All results cleared", 'info')

    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            if messagebox.askyesno("Exit", "Collection is in progress. Are you sure you want to exit?"):
                self.is_running = False
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Main application entry point"""
    try:
        # Check required modules
        required_modules = ['requests', 'dns.resolver', 'whois', 'PIL']
        missing_modules = []
        
        for module in required_modules:
            try:
                if module == 'dns.resolver':
                    import dns.resolver
                elif module == 'PIL':
                    from PIL import Image, ImageTk
                else:
                    __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            import tkinter.messagebox as mb
            mb.showerror(
                "Missing Dependencies",
                f"Please install required modules:\n\n" +
                "\n".join([f"pip install {mod}" for mod in missing_modules])
            )
            return
        
        # Create and run application
        collector = ModernOSINTCollector()
        root = collector.setup_gui()
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start GUI
        root.mainloop()
        
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror("Application Error", f"Failed to start application:\n{str(e)}")

if __name__ == "__main__":
    main()