import win32gui
import win32con
import win32process
import win32api

def focus_forza_window():
    window_name = "Forza Horizon 5"  # Verify exact title using window enumeration
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        print(f"Found window: {window_name}")
        try:
            # Get foreground window and threads
            fg_window = win32gui.GetForegroundWindow()
            current_thread = win32api.GetCurrentThreadId()
            fg_thread, _ = win32process.GetWindowThreadProcessId(fg_window)
            target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)

            # Attach input threads to allow SetForegroundWindow
            win32process.AttachThreadInput(current_thread, fg_thread, True)
            win32process.AttachThreadInput(current_thread, target_thread, True)

            # Restore and focus window
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            print("Successfully focused Forza Horizon 5")
            return True
        except Exception as e:
            print(f"Error focusing window: {e}")
            return False
        finally:
            # Detach input threads
            win32process.AttachThreadInput(current_thread, fg_thread, False)
            win32process.AttachThreadInput(current_thread, target_thread, False)
    else:
        print(f"Window '{window_name}' not found! Ensure FH5 is running and in windowed/borderless mode.")
        return False