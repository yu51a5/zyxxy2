########################################################################
## Draw With yyyyy (or yyyyy Drawings, or Drawing With yyyyy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

import numpy as np
from matplotlib.transforms import Bbox
from yyyyy_shape_style import _get_axes, get_default_text_bubble_params, get_linewidth_factor
from yyyyy_utils import atan, calc_Pythagoras
from yyyyy_shape_functions import draw_a_triangle
from yyyyy_colors import find_color_code
from yyyyy_bbox import ObjPosition

##################################################################
## TEXT                                                         ## 
##################################################################

class WordBubble:

  for s in ['left', 'right', 'bottom', 'top', 'center_x', 'center_y']:
    locals()[s] = ObjPosition(name=s)

  text_boxes = []
  all_objects = []

  ################################################################# 
  def get_all():
    return WordBubble.text_boxes

  ########################################################################
  def get_all_in_layers(layer_nbs=[], ax=None):
    ax = _get_axes(ax=ax)
    _tbs_in_layers = [as_ for as_ in WordBubble.all_objects if as_.get_axes() == ax]
    if len(layer_nbs) != 0:
      _tbs_in_layers = [sh for sh in _tbs_in_layers if sh.get_layer_nb() in layer_nbs]
    return _tbs_in_layers

  ################################################################# 
  def _create_params_subdictionary(param_names_dictionary, kwargs):
    result = {}
    used_argnames = []
    for dict_entry in param_names_dictionary:
      if isinstance(dict_entry, str):
        result[dict_entry] = kwargs[dict_entry] if dict_entry in kwargs else get_default_text_bubble_params(dict_entry)
        if dict_entry in kwargs:
          used_argnames += [dict_entry]
      else:
        result[dict_entry[0]] = kwargs[dict_entry[1]] if dict_entry[1] in kwargs else get_default_text_bubble_params(dict_entry[1])
        if dict_entry[1] in kwargs:
          used_argnames += [dict_entry[1]]
    return result, used_argnames

  ################################################################## 
  def __init__(self, text, x, y, ax=None, start=None, connection=None, **kwargs):

    WordBubble.all_objects.append(self)

    ax = _get_axes(ax=ax)
      
    props, used_argnames = WordBubble._create_params_subdictionary([['facecolor', 'background_color'], ['alpha', 'opacity'], 'pad', # 'rounding_size', 
    ['edgecolor', 'linecolor'], 'linewidth', ['zorder', 'layer_nb']], kwargs)
    props['boxstyle'] = 'round'
  
    text_dict, used_argnames2 = WordBubble._create_params_subdictionary(['fontsize', 'verticalalignment', 'horizontalalignment', 'multialignment', 'wrap', ['zorder', 'layer_nb'], 'fontfamily', 'color'], kwargs)
    used_argnames += used_argnames2

    _triangle = draw_a_triangle(tip=[0, 0], height=0, width=0, turn=0, color=props['facecolor'], 
                                outline_linewidth=props['linewidth']*get_linewidth_factor(), 
                                outline_color=props['edgecolor'],
                                layer_nb=props['zorder']+1/4, outline_layer_nb=props['zorder'])
    
    _triangle.set_visible(False)

    for dict_ in [props, text_dict]:
      for k in dict_.keys():
        if 'color' in k:
          dict_[k] = find_color_code(dict_[k])

    # place a text box in upper left in axes coords
    self.text_boxes = [ax.text(s=text, x=x, y=y, transform=ax.transData, **text_dict, bbox=props)]

    props['zorder'] += 1/2
    text_dict['zorder'] += 1/2
    props['edgecolor'] = 'none'
    props['facecolor'] = 'none'

    self.text_boxes.append(ax.text(s=text, x=x, y=y, transform=ax.transData, **text_dict, bbox=props))
    WordBubble.text_boxes += self.text_boxes

    if start is not None:
      connection = 'triangle'
    self.connection = connection
    self.start = start
    if start is None:
      self.connector = None
    else:
      assert connection in ['bubble', 'triangle']
      if  self.connection == 'triangle':
        self.connector = _triangle
        self.connector.shift_to(start)
        self.connector.width = kwargs['triangle_width'] if 'triangle_width' in kwargs else get_default_text_bubble_params('triangle_width')
        self.connector.set_visible(True)
      else:
        raise Exception("not implemented")
      self.set_text(text) # to adjust the size of the connector
    
    WordBubble.text_boxes.append(self)

  def get_axes(self):
    result = self.text_boxes[0].axes
    return result

  def get_layer_nb(self):
    result = self.text_boxes[0].get_zorder()
    return result

  def _get_what_to_move(self):
    result = self.text_boxes
    return result

  def make_visible(self, val=True):
    self.text_boxes[0].set_visible(val)
    self.text_boxes[1].set_visible(val)
    if self.connector is not None:
      self.connector.set_visible(val)

  def make_invisible(self):
    self.make_visible(False)

  def get_bbox(self):
    rend = self.get_axes().figure.canvas.get_renderer()
    tbb = self.text_boxes[0].get_window_extent(renderer=rend)
    abb = self.get_axes().get_window_extent(renderer=rend)
    a_xlim, a_ylim = self.get_axes().get_xlim(), self.get_axes().get_ylim()
    relative_width = tbb.width/abb.width * (a_xlim[1] - a_xlim[0])
    relative_height =  tbb.height/abb.height * (a_ylim[1] - a_ylim[0])

    xy = self.text_boxes[0].get_position()
    tbb_it = Bbox.from_extents(xy[0], xy[1], xy[0]+relative_width, xy[1]+relative_height)

    return tbb_it

  def shift_to_position(self, xy, position):

    # now adjust the position if needed
    new_xy = [xy[0], xy[1]]
    bbox = self.get_bbox()

    assert(position[0] in ['l', 'c', 'r'])
    if position[0] == 'c':
      new_xy[0] -= bbox.width/2
    elif position[0] == 'r':
      new_xy[0] -= bbox.width
    
    assert(position[1] in ['b', 'c', 't'])
    if position[1] == 'c':
      new_xy[1] -= bbox.height/2
    elif position[1] == 't':
      new_xy[1] -= bbox.height

    for tb in self.text_boxes:
      tb.set_position(new_xy)
    self.set_text(text=self.get_text())

  def shift(self, shift):
    for tb in self.text_boxes:
      tb.set_position(np.array(shift) + tb.get_position())

  def get_text(self):
    return self.text_boxes[0].get_text()

  def set_text(self, text, mid_override=None):
    self.text_boxes[0].set_text(text) 
    self.text_boxes[1].set_text(text)  
    tbb_it = self.get_bbox()
    mid = mid_override if mid_override is not None else [0.5*(tbb_it.x1+tbb_it.x0), 0.5*(tbb_it.y1+tbb_it.y0)]

    if self.connection is None:
      pass
    elif  self.connection == 'triangle':
      # xy is a top left corner
      triangle_height = calc_Pythagoras(self.start[0] - mid[0], self.start[1] - mid[1])
      self.connector.height = triangle_height
      triangle_turn = atan((self.start[0] - mid[0]) / (self.start[1] - mid[1]))
      if self.start[1] > mid[1]:
        triangle_turn += 6
      self.connector.turn_to(turn=triangle_turn)
    else:
      raise Exception("not implemented")

def draw_a_speech_bubble(text, x, y, position=None, **kwargs):
  wb = WordBubble(text, x, y, **kwargs)
  if position is not None:
    wb.shift_to_position(xy=[x, y], position=position)
  return wb
