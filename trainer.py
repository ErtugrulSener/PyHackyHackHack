import sys
from ctypes import *

import psutil

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
WriteProcessMemory = windll.kernel32.WriteProcessMemory


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

                hProcess = OpenProcess(
                    dwDesiredAccess,
                    bInheritHandle,
                    dwProccessId
                )

                return hProcess

        else:
            print(f"The process with the name: {processName} couldn't be found in process list!")

    """
        BOOL ReadProcessMemory(
            HANDLE  hProcess,
            LPCVOID lpBaseAddress,
            LPVOID  lpBuffer,
            SIZE_T  nSize,
            SIZE_T  *lpNumberOfBytesRead
        );
    """
    def ReadProcessMemory(self, hProcess, lpBaseAddress):
        try:
            # Create an unsigned integer buffer to read
            ReadBuffer = c_uint()

            # Reference the lpBuffer variable to ReadBuffer
            lpBuffer = byref(ReadBuffer)

            # Set nSize of the ReadBuffer
            nSize = sizeof(ReadBuffer)

            # Set a variable which you can use later to see what was read
            lpNumberOfBytesRead = c_ulong(0)

            ReadProcessMemory(
                hProcess,
                lpBaseAddress,
                lpBuffer,
                nSize,
                lpNumberOfBytesRead
            )

            return ReadBuffer.value

        except (BufferError, ValueError, TypeError):
            CloseHandle(hProcess)
            e = 'Handle Closed, Error 1', hProcess, GetLastError()
            return e

    """
        BOOL WriteProcessMemory(
            HANDLE  hProcess,
            LPCVOID lpBaseAddress,
            LPVOID  lpBuffer,
            SIZE_T  nSize,
            SIZE_T  *lpNumberOfBytesWritten
        );
    """
    def WriteProcessMemory(self, hProcess, lpBaseAddress, value):
        try:
            # Create an unsigned integer buffer to write
            WriteBuffer = c_uint(value)

            # Reference the lpBuffer variable to WriteBuffer
            lpBuffer = byref(WriteBuffer)

            # Set nSize of the WriteBuffer
            nSize = sizeof(WriteBuffer)

            # Set a variable which you can use later to see what was written
            lpNumberOfBytesWritten = c_ulong(0)

            WriteProcessMemory(
                hProcess,
                lpBaseAddress,
                lpBuffer,
                nSize,
                lpNumberOfBytesWritten
            )

            return WriteBuffer.value

        except (BufferError, ValueError, TypeError):
            CloseHandle(hProcess)
            e = 'Handle Closed, Error 2', hProcess, GetLastError()
            return e

    def CloseHandle(self, hObject):
        CloseHandle(hObject)

    def GetPointer(self, lpBaseAddress):
        pass


if __name__ == "__main__":
    mem = ReadWriteMemory()
    process = mem.OpenProcess(sys.argv[1])
    test = mem.WriteProcessMemory(process, 0x00E500A8, 5)

