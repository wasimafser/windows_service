import win32serviceutil
import win32service
import win32event
import servicemanager
import win32ts
import win32profile
import win32process
import win32con

import socket
import logging
import psutil
import sys

logging.basicConfig(filename="service.log", level=logging.DEBUG)


class ExampleService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AExampleService"
    _svc_display_name_ = "AExample Service"
    _svc_description_ = "Example description"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def main(self):
        """DO THE RUN STUFF HERE"""
        logging.info("SERVICE MAIN ENTERED !!")
        # 1. GET USER TOKEN
        console_session_id = win32ts.WTSGetActiveConsoleSessionId()
        console_user_token = win32ts.WTSQueryUserToken(console_session_id)

        # 2. GET THIS USER'S ENVIRONMENT
        environment = win32profile.CreateEnvironmentBlock(console_user_token, False)

        # 3. GENERATE STARTUPINFO FOR THE PROCESS ( OPTIONAL )
        startupInfo = win32process.STARTUPINFO()
        # OPTIONAL
        startupInfo.dwFlags = win32process.STARTF_USESHOWWINDOW
        startupInfo.wShowWindow = win32con.SW_NORMAL

        # 4. CREATE PROCESS AS USER
        win32process.CreateProcessAsUser(console_user_token,
                                         'notepad.exe',
                                         None,
                                         None,
                                         None,
                                         0,
                                         win32con.NORMAL_PRIORITY_CLASS,
                                         environment,
                                         None,
                                         startupInfo)



        # psutil.Popen('notepad.exe')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ExampleService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ExampleService)
