# setting MPLCONFIGDIR to suppress the warning
# see https://stackoverflow.com/questions/9827377/setting-matplotlib-mplconfigdir-consider-setting-mplconfigdir-to-a-writable-dir
import sys; sys.path.append('src')

from timeit import default_timer as timer
from zyxxy2 import nice_cat, wait_for_enter, shift_layers, stretch_layers, draw_a_circle, random_integer_number, is_the_same_point

canvas_width = 60
canvas_height = 39
light_radius = 10

head = nice_cat(axes_params=dict(canvas_width=60, canvas_height=39, tick_step=3,), block=False)
stretch_layers(diamond=head.diamond_coords, stretch=light_radius/4, layer_nbs=[1])
light = draw_a_circle(center=(30, 30), radius=light_radius, color='yellow', opacity=0.5, layer_nb=2, diamond_color='black')
while True:
  new_light_center = (float(random_integer_number(min=light_radius, max=canvas_width-light_radius)),
                      float(random_integer_number(min=light_radius, max=canvas_height-light_radius)))
  light.shift_to(new_light_center)
  while True:
    start = timer()
    cat_shift_str = wait_for_enter(f"Light is in {light.diamond_coords}. Cat is in {head.diamond_coords}. Enter cat shift! ")
    duration = timer() - start
    cat_shift = eval("(" + cat_shift_str + ")")
    
    shift_layers(shift=cat_shift, layer_nbs=[1])
    if (is_the_same_point(head.diamond_coords, light.diamond_coords)):
      wait_for_enter(f"Well done! Evaluation time: {int(duration)} seconds. Press ENTER to continue.")
      break

#from zyxxy2 import _run_all_tests
#_run_all_tests()

from zyxxy2 import try_shapes # demo_shape
#try_shapes(font_scaling=1)

from zyxxy2 import example_penguins # 
#example_penguins()

################################################################
# import draw_a_flag_of_Japan
# import draw_a_flag_of_Belgium
import draw_a_flag_of_Israel
# import draw_a_flag_of_Cuba
# import draw_a_flag_of_the_UK
# import draw_a_flag_of_Japanese_navy
# import draw_a_flag_of_the_USA

# import draw_a_cat
# import draw_a_stickman
# import draw_a_princess
# import draw_a_cat_with_gradient_fur
# import draw_a_xmas_tree
# import draw_simple_letters

# import demo_trigo

# import MY_yyyyy_demo_DUMP

# import draw_fancy_letters
# import draw_random_segments
# import draw_sun_and_moon
# import drawn_puzzle_circle
# import pythagoras_11
# import pythagoras_ab
# import drawn_puzzle_Pythagoras
# import draw_puzzle_segments
# import draw_rectangles 

# import draw_a_gradient
# import gradient_rectangle
# import catch_a_checker
# import draw_perspective
# import drawn_a_Coccinelle
# import drawn_blue_green_mandala

from zyxxy2 import *

# example_croc()
# example_penguins()
# example_yellow_cat()
draw_mandala_made_out_of_circles(color_inside='yellow')
# emoji_smiley()
# emoji_bee()
# emoji_apple()
# emoji_fish()
example_yellow_cat_animation()
# example_animated_croc()
