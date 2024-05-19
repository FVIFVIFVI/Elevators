from User_Interface_Components.button import Button

class ButtonFactory:
    @staticmethod
    def create_button(screen, posx, posy, width, height, text, shape="rect"):
        return Button(screen, posx, posy, width, height, text, shape)
