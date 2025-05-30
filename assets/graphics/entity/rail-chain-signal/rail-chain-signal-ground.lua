return
{
  structure =
  {
    layers =
    {
      util.sprite_load("__base__/graphics/entity/rail-chain-signal/rail-chain-signal",
        {
          priority = "high",
          frame_count = 4,
          direction_count = 16,
          scale = 0.5,
        }
      ),
      util.sprite_load("__base__/graphics/entity/rail-chain-signal/rail-chain-signal-lights",
        {
          priority = "low",
          blend_mode = "additive",
          draw_as_light = true,
          frame_count = 4,
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
    none   = 0,
    red    = 0,
    yellow = 1,
    green  = 2,
    blue   = 3,
  },

  rail_piece =
  {
    sprites = util.sprite_load(
      "__base__/graphics/entity/rail-chain-signal/rail-chain-signal-metals",
      {
        priority = "low",
        frame_count = 55,
        scale = 0.5,
      }
    ),
    render_layer = "rail-chain-signal-metal",
    align_to_frame_index =
    {
      --  X0Y0, X1Y0, X0Y1, X1Y1
      --  Left turn    | Straight/Multi   |  Right turn
      16, 16,  0,  0,  16, 16,  0,  0,  16, 16,  0,  0, -- North
       1, 17, 42, 38,   1, 17,  1, 17,  47, 17,  1, 26,
       2,  2, 18, 18,   2,  2, 18, 18,   2,  2, 18, 18,
      48,  3,  3,  3,   3,  3,  3,  3,   3, 27,  3, 39,
       4,  4,  4,  4,   4,  4,  4,  4,   4,  4,  4,  4, -- East
      28,  5, 40,  5,   5,  5,  5,  5,  46, 49,  5,  5,
       6,  6, 19, 19,   6,  6, 19, 19,   6,  6, 19, 19,
      20, 50, 43,  7,  20,  7, 20,  7,  20,  7, 41, 29,
      21, 21,  8,  8,  21, 21,  8,  8,  21, 21,  8,  8, -- South
      34, 30,  9, 22,   9, 22,  9, 22,   9, 44,  9, 51,
      10, 10, 23, 23,  10, 10, 23, 23,  10, 10, 23, 23,
      11, 11, 45, 52,  11, 11, 11, 11,  35, 11, 31, 11,
      12, 12, 12, 12,  12, 12, 12, 12,  12, 12, 12, 12, -- West
      13, 36, 13, 32,  13, 13, 13, 13,  13, 13, 53, 13,
      14, 14, 24, 24,  14, 14, 24, 24,  14, 14, 24, 24,
      25, 15, 54, 15,  25, 15, 25, 15,  33, 37, 25, 15,
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
    {0,0.15},{0,0.15},{0,0.15},{0,0.15},
    {0,0.15},{0,0.15},{0,0.15},{0,0.15},
    {0,0.15},{0,0.15},{0,0.15},{0,0.15},

    {0.12,0},{0.12,0},{0.12,0},{0.12,0},
    {0.12,0},{0.12,0},{0.12,0},{0.12,0},
    {0.12,0},{0.12,0},{0.12,0},{0.12,0},

    {0,0.15},{0,0.15},{0,0.15},{0,0.15},
    {0,0.15},{0,0.15},{0,0.15},{0,0.15},
    {0,0.15},{0,0.15},{0,0.15},{0,0.15},

    {0.12,0},{0.12,0},{0.12,0},{0.12,0},
    {0.12,0},{0.12,0},{0.12,0},{0.12,0},
    {0.12,0},{0.12,0},{0.12,0},{0.12,0},


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

    {0.12,0.12},{0.12,0.12},{0.12,0.12},{0.12,0.12},
    {0.12,0.12},{0.12,0.12},{0.12,0.12},{0.12,0.12},
    {0.12,0.12},{0.12,0.12},{0.12,0.12},{0.12,0.12},


    -- West
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},

    {0,0.12},{0,0.12},{0,0.12},{0,0.12},
    {0,0.12},{0,0.12},{0,0.12},{0,0.12},
    {0,0.12},{0,0.12},{0,0.12},{0,0.12},

    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},
    {0,0},{0,0},{0,0},{0,0},

    {0,0.12},{0,0.12},{0,0.12},{0,0.12},
    {0,0.12},{0,0.12},{0,0.12},{0,0.12},
    {0,0.12},{0,0.12},{0,0.12},{0,0.12},
  },
  lights =
  {
    green  = { light = {intensity = 0.2, size = 4, color={0,   1,   0 }}, shift = { 0, 0 }},
    yellow = { light = {intensity = 0.2, size = 4, color={1,   0.5, 0 }}, shift = { 0, 0 }},
    red    = { light = {intensity = 0.2, size = 4, color={1,   0,   0 }}, shift = { 0, 0 }},
    blue   = { light = {intensity = 0.2, size = 4, color={0.4, 0.4, 1 }}, shift = { 0, 0 }},
  },
  circuit_connector = circuit_connector_definitions["rail-chain-signal"],
}
