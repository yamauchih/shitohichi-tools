--
-- convert 3dsmax shaders to mia_material (Arch&Design) shader
-- Author:  Shitohich Umaya
-- Created: 12.4.2010
--
-- based on Zap's V-Ray material converter
-- (see http://mentalraytips.blogspot.com/)
--


--
-- use material object map array
--
fileIn "yh_material_object_map.ms"


----------------------------------------------------------------------
-- file local
G_unknown_mat_count   = 0
G_converted_mat_count = 0

--
-- Standard Materials to mia_material
--
function yh_get_mia_mat_from_standard_mat std_mat =
(
    -- check the material
    -- print (format "Here is std: [%]. " (classof std_mat))
    if (classof std_mat) != Standardmaterial then (
        throw "Error! not a Standardmaterial"
    )

    -- create new mia_material
    new_mat = mrArchMaterial()

    -- mark as converted
    new_mat.name = "m2mmconv_" + std_mat.name

    new_mat.opts_backface_cull = not std_mat.twosided

    ----------------------------------------
    -- diffuse
    ----------------------------------------
    new_mat.diff_color        = std_mat.diffuse
    new_mat.diff_color_map    = std_mat.maps[2]
    new_mat.diff_weight       = std_mat.mapAmounts[2] / 100
    new_mat.diff_color_map_on = std_mat.mapEnables[2]


    ----------------------------------------
    -- specular color
    ----------------------------------------
    new_mat.refl_color        = std_mat.specular
    new_mat.refl_color_map    = std_mat.maps[3]
    new_mat.refl_color_map_on = std_mat.mapEnables[3]
    new_mat.refl_weight       = std_mat.mapAmounts[3] / 100

    ----------------------------------------
    -- specular level
    ----------------------------------------
    new_mat.refl_weight       = std_mat.specularLevel /100

    ----------------------------------------
    -- glossiness
    ----------------------------------------
    new_mat.refl_gloss        = std_mat.glossiness /100
    new_mat.refl_gloss_map    = std_mat.maps[5]
    new_mat.refl_gloss_map_on = std_mat.mapEnables[5]

    ----------------------------------------
    -- bumpmap
    ----------------------------------------
    new_mat.bump_map          = std_mat.maps[9]
    new_mat.bump_map_on       = std_mat.mapEnables[9]
    new_mat.bump_map_amt      = std_mat.mapAmounts[9] /100

    ----------------------------------------
    -- displacement
    ----------------------------------------
    new_mat.displacement_map_on  = std_mat.mapEnables[12]
    new_mat.displacement_map     = std_mat.maps[12]
    new_mat.displacement_map_amt = std_mat.mapAmounts[12] / 100

    return new_mat
)

--
-- multi-material
--
function yh_get_mia_mat_from_multi_mat mul_mat =
(
    if (classof mul_mat) != MultiMaterial then (
        throw "Error! not a MultiMaterial"
    )

    -- create new
    new_mat = multimaterial numsubs:mul_mat.numsubs

    -- mark as converted
    new_mat.name = "m2mmconv_" + mul_mat.name

    -- for all sub material: replace all
    for i = 1 to mul_mat.numsubs do
    (
        sub_mat = (yh_convert_any_mat_to_mia_mat mul_mat.materialList[i])
        -- print (format "   submat = % " sub_mat.name)
        new_mat.materialList[i] = sub_mat
    )

    return new_mat
)

--
-- material conversion message helper
--
function yh_conv_mes m1 m2 =
(
    print (format "converting (%) [%] -> (%) [%]. " \
            (classof m1) m1.name (classof m2) m2.name)
)

--
--  Convert Material Function
--  param[in] mat material to be converted
--  return    converted material
--
function yh_convert_any_mat_to_mia_mat mat =
(
    -- print (format "classof mat = [%], name = %. " (classof mat) mat.name)
    if (findString mat.name "m2mmconv_") == 1 then (
        -- this is already converted
        print (format "This has been converted. name = %. " mat.name)
        return mat
    )

    case classof mat of
    (
    Standardmaterial:
    (
        new_mat = (yh_get_mia_mat_from_standard_mat mat)
        yh_conv_mes mat new_mat

        G_converted_mat_count = G_converted_mat_count + 1
        return new_mat
    )

    MultiMaterial:
    (
        new_mat = yh_get_mia_mat_from_multi_mat mat
        yh_conv_mes mat new_mat

        G_converted_mat_count = G_converted_mat_count + 1
        return new_mat
    )

    Arch___Design__mi:
    (
        -- no need to convert: count as succeeded
        G_converted_mat_count = G_converted_mat_count + 1
		new_mat = mat
        return new_mat
    )
    -- These should be handled sorta like Blend above...
    -- CompositeMaterial: return()
    -- DoubleSided: return()
    -- Ink__n_Paint: return()
    -- MatteShadow: return()
    -- MorpherMaterial: return()
    -- MatEval_Test_Mat: return()
    -- Shellac: return()
    -- TopBottom: return()
    default:
    (
        print "Unknown material"
        G_unknown_mat_count = G_unknown_mat_count + 1
        -- new_mat.name = "unknown_" + mat.name
    )

    ) -- case class of mat

    -- return original one.
    return mat
)


--
-- convert all materials in the scene
--
function yh_convert_all_material =
(
    -- reset global variables
    G_unknown_mat_count   = 0
    G_converted_mat_count = 0

    -- mat_ary: array of { material name, material index } ,
    local mat_ary     = yh_collect_material();
    -- mat_obj_array: mat_obj_array[material_index][index_of_geometry_of_the_same_materias]
    -- sceneMaterials[material_index] gives material
    local mat_obj_ary = yh_create_material_object_array mat_ary;

    print (format "shader count = %. " mat_ary.count)
    local total_geom = 0
    for i = 1 to mat_ary.count  do
    (
        total_geom = total_geom + mat_obj_ary[i].count
    )

    -- Check the consistency
    (yh_check_consistency_material_object_map mat_obj_ary)

    -- convert all materials
    local unknown_mat_count = 0
    local conv_mat_count    = 0
    local orgSceneMaterials = sceneMaterials
    for i = 1 to orgSceneMaterials.count do
    (
        mat = orgSceneMaterials[i]
        new_mat = yh_convert_any_mat_to_mia_mat mat

        for j = 1 to mat_obj_ary[i].count do
        (
            mat_obj_ary[i][j].material = new_mat
        )
        print (format "Converted % -> % ." mat.name new_mat.name)
    )

    print (format "% materials are converted. % are unknown. " \
        G_converted_mat_count G_unknown_mat_count)
)


(
        disableSceneRedraw()
        setWaitCursor()

        local t_start = 1.0 * timestamp()

        yh_convert_all_material()

        local total_time =(timestamp() - t_start)
        print (format "Elapsed time %ms. " total_time)

        setArrowCursor()
        enableSceneRedraw()
        completeredraw()

)
