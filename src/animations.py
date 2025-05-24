from PyQt5.QtCore import QPropertyAnimation, QEasingCurve


class AnimationManager:
    def __init__(self):
        pass

    def animate_sidebar(self, sidebar):
        try:
            animation = QPropertyAnimation(sidebar, b"maximumWidth")
            animation.setDuration(300)
            animation.setStartValue(100)
            animation.setEndValue(200)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.start()
        except Exception as e:
            print(f"Error in animate_sidebar: {e}")
            raise
