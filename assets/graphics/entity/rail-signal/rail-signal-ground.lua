return
{
  structure =
  {
    layers =
    {
      util.sprite_load("__base__/graphics/entity/rail-signal/rail-signal",
        {
          priority = "high",
          frame_count = 3,
          direction_count = 16,
          scale = 0.5,
        }
      ),
      util.sprite_load("__base__/graphics/entity/rail-signal/rail-signal-lights",
        {
          priority = "low",
          blend_mode = "additive",
          draw_as_light = true,
          frame_count = 3,
          direction_count = 16,
          scale = 0.5,
        }
      ),
    }
  },
  structure_render_layer = "floor-mechanics",
  structure_align_to_animation_index =
  {
    --  X0Y0, X1Y0, X0Y1, X1Y1
    --  Left turn  | Straight/Multi |  Right turn
     0,  0,  0,  0,   0,  0,  0,  0,   0,  0,  0,  0, -- North
     1,  1,  1,  1,   1,  1,  1,  1,   1,  1,  1,  1,
     2,  2,  2,  2,   2,  2,  2,  2,   2,  2,  2,  2,
     3,  3,  3,  3,   3,  3,  3,  3,   3,  3,  3,  3,
     4,  4,  4,  4,   4,  4,  4,  4,   4,  4,  4,  4, -- East
     5,  5,  5,  5,   5,  5,  5,  5,   5,  5,  5,  5,
     6,  6,  6,  6,   6,  6,  6,  6,   6,  6,  6,  6,
     7,  7,  7,  7,   7,  7,  7,  7,   7,  7,  7,  7,
     8,  8,  8,  8,   8,  8,  8,  8,   8,  8,  8,  8, -- South
     9,  9,  9,  9,   9,  9,  9,  9,   9,  9,  9,  9,
    10, 10, 10, 10,  10, 10, 10, 10,  10, 10, 10, 10,
    11, 11, 11, 11,  11, 11, 11, 11,  11, 11, 11, 11,
    12, 12, 12, 12,  12, 12, 12, 12,  12, 12, 12, 12, -- West
    13, 13, 13, 13,  13, 13, 13, 13,  13, 13, 13, 13,
    14, 14, 14, 14,  14, 14, 14, 14,  14, 14, 14, 14,
    15, 15, 15, 15,  15, 15, 15, 15,  15, 15, 15, 15,
  },
  signal_color_to_structure_frame_index =
  {
    green  = 0,
    yellow = 1,
    red    = 2,
  },

  rail_piece =
  {
    sprites = util.sprite_load(
      "__base__/graphics/entity/rail-signal/rail-signal-metals",
      {
        priority = "low",
        frame_count = 50,
        scale = 0.5,
      }
    ),
    render_layer = "rail-chain-signal-metal",
    align_to_frame_index =
    {

      --  X0Y0, X1Y0, X0Y1, X1Y1
      --  Left turn    | Straight/Multi   |  Right turn
       0,  0, 16, 16,   0,  0, 16, 16,   0,  0, 16, 16, -- North
       1, 17,  1, 38,   1, 17,  1, 17,  42, 17,  1, 26,
       2,  2, 18, 18,   2,  2, 18, 18,   2,  2, 18, 18,
      43,  3,  3,  3,   3,  3,  3,  3,   3, 27,  3, 39,
       4,  4,  4,  4,   4,  4,  4,  4,   4,  4,  4,  4, -- East
      28,  5,  5,  5,   5,  5,  5,  5,  40, 44,  5,  5,
       6, 19,  6, 19,   6, 19,  6, 19,   6, 19,  6, 19,
      20, 45, 20,  7,  20,  7, 20,  7,  20,  7, 41, 29,
       8,  8, 21, 21,   8,  8, 21, 21,   8,  8, 21, 21, -- South
      34, 30,  9, 22,   9, 22,  9, 22,   9, 22,  9, 46,
      10, 10, 23, 23,  10, 10, 23, 23,  10, 10, 23, 23,
      11, 11, 35, 47,  11, 11, 11, 11,  11, 11, 31, 11,
      12, 12, 12, 12,  12, 12, 12, 12,  12, 12, 12, 12, -- West
      13, 36, 13, 32,  13, 13, 13, 13,  13, 13, 48, 13,
      14, 14, 24, 24,  14, 14, 24, 24,  14, 14, 24, 24,
      25, 15, 49, 15,  25, 15, 25, 15,  33, 37, 25, 15,
    }
  },
  selection_box_shift =
  {
    -- Given this affects SelectionBox, it is part of game state.
    -- NOTE: Those shifts are not processed (yet) by PrototypeAggregateValues::calculateBoxExtensionForSelectionBoxSearch()
    --    so if you exceed some reasonable values, a signal may become unselectable
    -- NOTE: only applies to normal selection box. It is ignored for chart selection box
    --

    --  X0Y0, X1Y0, X0Y1, X1Y1

    -- North -- 0
    {0,0},{0,0},{0,0},{0,0}, --  Left turn
    {0,0},{0,0},{0,0},{0,0}, --  Straight/Multi
    {0,0},{0,0},{0,0},{0,0}, --  Right turn

    {-0.12,0},{-0.12,0},{-0.12,0},{-0.12,0},
    {-0.12,0},{-0.12,0},{-0.12,0},{-0.12,0},
    {-0.12,0},{-0.12,0},{-0.12,0},{-0.12,0},

    {0.2,0.2},{0.2,0.2},{0.2,0.2},{0.2,0.2},
    {0.2,0.2},{0.2,0.2},{0.2,0.2},{0.2,0.2},
    {0.2,0.2},{0.2,0.2},{0.2,0.2},{0.2,0.2},

    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},


    -- East
    {0,0.25},{0,0.25},{0,0.25},{0,0.25},
    {0,0.25},{0,0.25},{0,0.25},{0,0.25},
    {0,0.25},{0,0.25},{0,0.25},{0,0.25},

    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},

    {0,0.25},{0,0.25},{0,0.25},{0,0.25},
    {0,0.25},{0,0.25},{0,0.25},{0,0.25},
    {0,0.25},{0,0.25},{0,0.25},{0,0.25},

    {0.18,-0.15},{0.18,-0.15},{0.18,-0.15},{0.18,-0.15},
    {0.18,-0.15},{0.18,-0.15},{0.18,-0.15},{0.18,-0.15},
    {0.18,-0.15},{0.18,-0.15},{0.18,-0.15},{0.18,-0.15},


    -- South
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},

    {0.15,0},{0.15,0},{0.15,0},{0.15,0},
    {0.15,0},{0.15,0},{0.15,0},{0.15,0},
    {0.15,0},{0.15,0},{0.15,0},{0.15,0},

    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},

    {0,0.12},{0,0.12},{0,0.12},{0,0.12},
    {0,0.12},{0,0.12},{0,0.12},{0,0.12},
    {0,0.12},{0,0.12},{0,0.12},{0,0.12},


    -- West
    {0,-0.12},{0,-0.12},{0,-0.12},{0,-0.12},
    {0,-0.12},{0,-0.12},{0,-0.12},{0,-0.12},
    {0,-0.12},{0,-0.12},{0,-0.12},{0,-0.12},

    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},

    {0,-0.12},{0,-0.12},{0,-0.12},{0,-0.12},
    {0,-0.12},{0,-0.12},{0,-0.12},{0,-0.12},
    {0,-0.12},{0,-0.12},{0,-0.12},{0,-0.12},

    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
  },
  lights =
  {
    green  = { light = {intensity = 0.2, size = 4, color={r=0, g=1,   b=0 }}, shift = { 0, -0.5 }},
    yellow = { light = {intensity = 0.2, size = 4, color={r=1, g=0.5, b=0 }}, shift = { 0,  0   }},
    red    = { light = {intensity = 0.2, size = 4, color={r=1, g=0,   b=0 }}, shift = { 0,  0.5 }},
  },
  circuit_connector = circuit_connector_definitions["rail-signal"],
}