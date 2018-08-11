RED = "red"
GREEN = "green"
BLUE = "blue"


def get_double_colors(hex_color: str) -> dict:
    COLOR_MAX: int = 255
    math_colors: dict = {}
    hex_color: str = hex_color.replace('#', '')
    if len(hex_color) == 6:
        red: str = hex_color[0:2]
        green: str = hex_color[2:4]
        blue: str = hex_color[4:7]

        try:
            math_colors[RED]: int = int(red, 16) / COLOR_MAX
            math_colors[GREEN]: int = int(green, 16) / COLOR_MAX
            math_colors[BLUE]: int = int(blue, 16) / COLOR_MAX
            return math_colors  # RETURN
        except:
            raise AttributeError("Color is not are hex number {%s}" % hex_color)

    # NOT CALL IF COLOR LENGTH EQUAL 6
    raise AttributeError("Color length must be 6, but is now " + str(len(hex_color)))
