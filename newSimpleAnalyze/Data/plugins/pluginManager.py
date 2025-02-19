from Data.plugins.plugin import Plugin

class PluginManager:
    def __init__(self):
        self.windows_plugins = []
        self.mac_plugins = []
        self.linux_plugins = []
        self.load_windows_plugins()
        self.load_mac_plugins()
        self.load_linux_plugins()

    def load_windows_plugins(self):
        plugin_data = [
            {
                "name": "windows.pslist",
                "description": "Displays a detailed list of all running processes on a system."
            },
            {
                "name": "windows.cmdline",
                "description": "Shows the command line arguments passed to each process."
            },
            {
                "name": "windows.dlllist",
                "description": "Lists the Dynamic Link Libraries (DLLs) loaded into each process's address space."
            },
            {
                "name": "windows.info",
                "description": "Provides detailed information about the operating system and kernel from a Windows memory dump."
            },
            {
                "name": "windows.psscan",
                "description": "Shows a list of processes running on a system."
            },
            {
                "name": "windows.pstree",
                "description": "Shows the process tree of the system."
            },
            {
                "name": "windows.psxview",
                "description": "Reveals hidden processes."
            },
            {
                "name": "windows.privs",
                "description": "Shows the privileges of processes running on a system."
            },
            {
                "name": "windows.svcscan",
                "description": "Inspects Windows services."
            },
            {
                "name": "windows.memmap",
                "description": "Shows memory areas and access permissions."
            },
            {
                "name": "windows.memdump",
                "description": "Dumps the process memory to a file."
            },
            {
                "name": "windows.mutantscan",
                "description": "Inspects the Object."
            },
            {
                "name": "windows.driverscan",
                "description": "Inspects loaded kernel drivers."
            },
            {
                "name": "windows.iehistory",
                "description": "Extracts the usage history of the Internet Explorer browser."
            },
            {
                "name": "windows.consoles",
                "description": "Shows processes with open consoles."
            },
            {
                "name": "windows.getsids",
                "description": "Displays security identifiers (SIDs) for a process."
            },
            {
                "name": "windows.vadinfo",
                "description": "Shows details about Virtual Address Descriptors."
            },
            {
                "name": "windows.modscan",
                "description": "Inspects potentially harmful kernel modules."
            },
            {
                "name": "windows.ldrmodules",
                "description": "Shows the loaded modules."
            },
            {
                "name": "windows.dlllist_cache",
                "description": "Shows DLL libraries stored in the cache."
            },
            {
                "name": "windows.malfind",
                "description": "Finds injected code and other infections."
            },
            {
                "name": "windows.handles",
                "description": "Finds injected code and other exceptions."
            },
            {
                "name": "windows.devicetree",
                "description": "Shows the device tree of the process."
            },
            {
                "name": "windows.mbrparser",
                "description": "Analyzes the Master Boot Record (MBR)."
            },
            {
                "name": "windows.userassist",
                "description": "Extracts information about the UserAssist."
            },
            {
                "name": "windows.shellbags",
                "description": "Retrieves information from Windows shell folders."
            }
        ]
        self.windows_plugins = [Plugin(**plugin) for plugin in plugin_data]

    def load_mac_plugins(self):
        plugin_data = [
            {
                "name": "mac.bash.Bash",
                "description": "Recovers the bash command history from a system's memory."
            },
            {
                "name": "mac.yarascan",
                "description": "Scans memory with YARA rules."
            },
            {
                "name": "mac.volshell",
                "description": "Provides an interactive Volatility shell for advanced analysis."
            },
            {
                "name": "mac.vma",
                "description": "Displays virtual memory areas for processes."
            },
            {
                "name": "mac.threads",
                "description": "Lists threads for processes."
            },
            {
                "name": "mac.tasks",
                "description": "Lists kernel tasks."
            },
            {
                "name": "mac.system_info",
                "description": "Displays general system information."
            },
            {
                "name": "mac.sysctl",
                "description": "Displays sysctl information."
            },
            {
                "name": "mac.strings",
                "description": "Extracts strings from memory."
            },
            {
                "name": "mac.socket_filters",
                "description": "Lists socket filters."
            },
            {
                "name": "mac.sockets",
                "description": "Lists open sockets."
            },
            {
                "name": "mac.psxview",
                "description": "Cross-references process listings from various sources."
            },
            {
                "name": "mac.pslist",
                "description": "Displays a list of running processes."
            },
            {
                "name": "mac.proc_maps",
                "description": "Lists process memory maps."
            },
            {
                "name": "mac.proc_info",
                "description": "Displays detailed process information."
            },
            {
                "name": "mac.pmap",
                "description": "Lists physical memory regions."
            },
            {
                "name": "mac.mount",
                "description": "Lists mounted filesystems."
            },
            {
                "name": "mac.macho",
                "description": "Parses Mach-O headers."
            },
            {
                "name": "mac.list_sessions",
                "description": "Lists login sessions."
            },
            {
                "name": "mac.list_files",
                "description": "Lists open files for each process."
            },
            {
                "name": "mac.kpcrash",
                "description": "Lists kernel panic logs."
            },
            {
                "name": "mac.kevents",
                "description": "Lists kernel events."
            },
            {
                "name": "mac.ifconfig",
                "description": "Displays network interface configuration."
            },
            {
                "name": "mac.hostfiles",
                "description": "Extracts host files from memory."
            },
            {
                "name": "mac.dump_files",
                "description": "Dumps files from memory."
            },
            {
                "name": "mac.dmesg",
                "description": "Displays system messages."
            },
            {
                "name": "mac.dead_procs",
                "description": "Lists terminated processes."
            },
            {
                "name": "mac.dead_tasks",
                "description": "Lists terminated kernel tasks."
            },
            {
                "name": "mac.check_syscalls",
                "description": "Checks for hooked syscalls."
            }
        ]
        self.mac_plugins = [Plugin(**plugin) for plugin in plugin_data]

    def load_linux_plugins(self):
        plugin_data = [
            {
                "name": "linux.bash",
                "description": "Extracts bash command history from memory."
            },
            {
                "name": "linux.cpuinfo",
                "description": "Displays CPU information."
            },
            {
                "name": "linux.dmesg",
                "description": "Displays the kernel ring buffer messages."
            },
            {
                "name": "linux.gdbserver",
                "description": "Identifies and inspects gdbserver processes."
            },
            {
                "name": "linux.iomem",
                "description": "Lists memory-mapped I/O regions."
            },
            {
                "name": "linux.keyboard_notifiers",
                "description": "Lists kernel keyboard notifiers."
            },
            {
                "name": "linux.ldrmodules",
                "description": "Displays loaded kernel modules."
            },
            {
                "name": "linux.lsmod",
                "description": "Lists loaded kernel modules."
            },
            {
                "name": "linux.lsof",
                "description": "Lists open files for each process."
            },
            {
                "name": "linux.malfind",
                "description": "Finds injected code and other infections."
            },
            {
                "name": "linux.netstat",
                "description": "Displays network connections."
            },
            {
                "name": "linux.proc_maps",
                "description": "Lists process memory maps."
            },
            {
                "name": "linux.proc_info",
                "description": "Displays detailed process information."
            },
            {
                "name": "linux.psaux",
                "description": "Displays processes with full command line arguments."
            },
            {
                "name": "linux.pslist",
                "description": "Lists running processes."
            },
            {
                "name": "linux.pstree",
                "description": "Displays a tree of running processes."
            },
            {
                "name": "linux.psxview",
                "description": "Cross-references process listings from various sources."
            },
            {
                "name": "linux.sockets",
                "description": "Lists open sockets."
            },
            {
                "name": "linux.strings",
                "description": "Extracts strings from memory."
            },
            {
                "name": "linux.timers",
                "description": "Lists kernel timers."
            },
            {
                "name": "linux.vma",
                "description": "Displays virtual memory areas for processes."
            }
        ]
        self.linux_plugins = [Plugin(**plugin) for plugin in plugin_data]

    def get_plugins(self, os_type):
        if os_type == 'windows':
            self.load_windows_plugins()
            return self.windows_plugins
        elif os_type == 'mac':
            self.load_mac_plugins()
            return self.mac_plugins
        elif os_type == 'linux':
            self.load_linux_plugins()
            return self.linux_plugins
        else:
            raise ValueError(f"Unsupported OS type: {os_type}")

