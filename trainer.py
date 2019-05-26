import sys
from ctypes import *

import psutil

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

class ReadWriteMemory:

    """
        HANDLE OpenProcess(
            DWORD dwDesiredAccess,
            BOOL  bInheritHandle,
            DWORD dwProcessId
        );
    """
    def OpenProcess(self, processName):
        dwDesiredAccess = (PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE)
        bInheritHandle = False

        for process in psutil.process_iter():
            if process.name() == processName:
                dwProccessId = process.pid

                hProcess = (
                    dwDesiredAccess,
                    bInheritHandle,
                    dwProccessId
                );

                return hProcess

        else:
            print(f"The process with the name: {processName} couldn't be found in process list!")

    def CloseHandle(self, hObject):
        CloseHandle(hObject)

    def GetLastError(self):
        pass


if __name__ == "__main__":
    mem = ReadWriteMemory()
    mem.OpenProcess(sys.argv[1])
