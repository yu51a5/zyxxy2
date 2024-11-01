import numpy as np
from matplotlib.colors import is_color_like, to_rgb
from MY_yyyyy_SETTINGS_general import my_color_palette
from yyyyy_utils import find_LCM, get_sign, is_the_same_point, is_a_number
from math import floor

##################################################################
## color HELPERS                                               ## 
##################################################################

def find_color_code(color_name):
  if color_name is None or (isinstance(color_name, str) and color_name == 'none'):
    return 'none'
  if isinstance(color_name, str) and color_name in my_color_palette:
    return np.array(to_rgb(my_color_palette[color_name]))
  if is_a_number(color_name):
    return find_color_code([color_name, color_name, color_name])
  if not is_color_like(color_name):
    raise Exception(color_name, "is not a valid color!")
  return np.array(to_rgb(color_name))

##################################################################
def colors_are_equal(color_1, color_2):
  color_code_1, color_code_2 = find_color_code(color_1), find_color_code(color_2)
  if color_code_1.size == 3:
    color_code_1 = np.append(color_code_1, 1.)
  if color_code_2.size == 3:
    color_code_2 = np.append(color_code_2, 1.)
  return is_the_same_point(color_code_1, color_code_2)

##################################################################
def get_color_mix(color_1, proportion_of_color_1, color_2):
  color_code_1, color_code_2 = find_color_code(color_1), find_color_code(color_2)
  return color_code_1 * proportion_of_color_1 + (1. - proportion_of_color_1) * color_code_2

def get_color_tone(color, proportion_of_color):
  result = get_color_mix(color_1=color, proportion_of_color_1=proportion_of_color, color_2='#808080')
  return result

def get_color_tint(color, proportion_of_color):
  result = get_color_mix(color_1=color, proportion_of_color_1=proportion_of_color, color_2='white')
  return result

def get_color_shade(color, proportion_of_color):
  result = get_color_mix(color_1=color, proportion_of_color_1=proportion_of_color, color_2='black')
  return result

##################################################################
def create_gradient_colors(rgb_start, rgb_end, nb_steps=None): 

  rgb_start_, rgb_end_ = find_color_code(rgb_start), find_color_code(rgb_end)

  if nb_steps <= 1:
    return [rgb_end_]

  if nb_steps is None:
    nb_steps_per_channel = [int(abs(rgb_start_elem - rgb_end_elem)+1) for rgb_start_elem, rgb_end_elem in zip(rgb_start_, rgb_end_)]

    nb_steps = 1
    for nspc in nb_steps_per_channel:
      nb_steps = find_LCM(n=nspc, m=nb_steps)

    result = np.array([rgb_start_ for _ in range(nb_steps)], dtype=np.float64)
    for i, (nspc, rgb_s, rgb_e) in enumerate(zip(nb_steps_per_channel, rgb_start_, rgb_end_)):
      size_of_the_step = int(nb_steps / nspc)
      for j in range(nspc):
        result[j*size_of_the_step : (j+1)*size_of_the_step, i] += get_sign(rgb_e-rgb_s) * j

    result /= 255.
  else:
    rgb_start_np, rgb_end_np = np.array(rgb_start_, dtype=np.float64), np.array(rgb_end_, dtype=np.float64)
    result = [(i*rgb_end_np + (nb_steps-1-i)*rgb_start_np)/(nb_steps-1) for i in range(nb_steps)]
    if np.max([rgb_start_np, rgb_end_np]) > 1:
      result = [r / 255. for r in result]

  return result

#######################################################
def get_multi_gradient_color(colors, how_many=200, color_limits=None):

    assert len(colors) >= 2
    assert (not color_limits) or (len(colors) == (len(color_limits) + 2))
    if len(colors) == 2:
      assert not color_limits
      color_limits = []
    elif not color_limits:
      color_limits = [i/(len(colors) - 1) for i in range(1, len(colors)-1)]
    
    color_limits2 = [0] + color_limits + [1]
    error_is  = [i for i, l in enumerate(color_limits2) if i > 0 and color_limits2[i-1] > l]
    assert not error_is, f'Points with indices {error_is} are out of order in {color_limits2}'

    fractions = [(l - color_limits2[i-1]) / (color_limits2[-1] - color_limits2[0]) 
                              for i, l in enumerate(color_limits2) if i > 0]
    nb_rectanles = [floor(f * (how_many - 1)) for f in fractions]
    indices_fractions = [[i, f-floor(f)] for i, f in enumerate(fractions)]
    indices_fractions.sort(key = lambda i_f : -i_f[1])
    diff = how_many - 1 - sum(nb_rectanles)
    for d in range(diff):
      nb_rectanles[indices_fractions[d][0]] += 1

    result_colors = [find_color_code(colors[0])]
    for i, l in enumerate(colors):
      if i > 0:
        result_colors = result_colors[:-1] + create_gradient_colors(rgb_start=colors[i-1], 
                                                                    rgb_end=l, 
                                                                    nb_steps=nb_rectanles[i-1]+1)

  
    return result_colors
