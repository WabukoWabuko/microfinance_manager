from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect

class AnimationManager:
    def __init__(self):
        try:
            print("AnimationManager initialized")
        except Exception as e:
            print(f"Error in AnimationManager.__init__: {e}")
            raise

    def animate_sidebar(self, sidebar):
        try:
            # Start sidebar off-screen (left)
            start_rect = QRect(-sidebar.width(), sidebar.y(), sidebar.width(), sidebar.height())
            end_rect = QRect(0, sidebar.y(), sidebar.width(), sidebar.height())
            sidebar.setGeometry(start_rect)
            animation = QPropertyAnimation(sidebar, b"geometry")
            animation.setDuration(300)
            animation.setStartValue(start_rect)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.start()
            print("Sidebar animation started")
        except Exception as e:
            print(f"Error in animate_sidebar: {e}")
            raise

    def close(self):
        try:
            print("AnimationManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
