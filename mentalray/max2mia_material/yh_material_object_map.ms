--
-- material object map creation.
-- Author:  Yamauchi Hitoshi
-- Created: 15.4.2010
--

--
-- material name index pair
--
struct yh_material_object_index_pair (
    -- name of material
    m_name,
    -- index of material of sceneMaterials
    m_index
)

--
-- material name comparison function
--
function yh_material_object_index_pair_name_comp s1 s2 =
(
    if  s1.m_name > s2.m_name then 1
    else (
        -- need == 0 to find the item for bsearch
        if s1.m_name < s2.m_name then -1 else 0
    )
)

--
-- make an index array of materials
--
-- return material name index pair array
--
function yh_collect_material =
(
    local orgSceneMaterials = sceneMaterials
    local mat_ary = #()

    -- print (format "geometry count = %\n" geometry.count)

    -- I could not find hash function in max script.
    --
    -- the same name shader can not exist in the scene, so we could
    -- use it an identifier of shaders.

	-- m_name: is struct initialization by name, like pascal, see manual struct
    for i = 1 to orgSceneMaterials.count do
    (
        mat_ary[i] = yh_material_object_index_pair m_name:orgSceneMaterials[i].name m_index:i
    )

    -- for i = 1 to mat_ary.count do
    -- (
    --     print (format  "Orig  : [%]: %\n" mat_ary[i].m_index mat_ary[i].m_name);
    -- )

    qsort mat_ary yh_material_object_index_pair_name_comp

    -- for i = 1 to mat_ary.count do
    -- (
    --     print (format "Sorted:  [%]: %\n" mat_ary[i].m_index mat_ary[i].m_name);
    -- )

    return mat_ary
)

--
-- create material object array
--
-- param mat_ary material name and index struct array created by
-- yh_collect_material.
--
-- returns mat_obj_ary[material_index][geometry_index]
--
function yh_create_material_object_array mat_ary =
(
    -- multi dimensional array
    mat_obj_ary = #();
    for i = 1 to mat_ary.count do
    (
        mat_obj_ary[i] = #(); -- array in array
    )

    local percent_count = geometry.count / 100;
    -- if 0, mod casts error, set to 100.
    if percent_count == 0 then (
		percent_count = 100
    )

    local geoidx = 0
	local undef_mat_geo = 0
	-- check all the geometry has the material or not
	for geoidx = 1 to geometry.count do
    (
		if geometry[geoidx].material == undefined then (
			undef_mat_geo = undef_mat_geo + 1
			print (format "Error! geometry [%] has no material assigned. Can not convert no material.\n" geoidx)
		)
	)
	if undef_mat_geo > 0 then (
		print (format "Error! there are % geometries that has no material. Abort.\n" undef_mat_geo)
		throw "Error! some geometry has no material."
	)

    for geoidx = 1 to geometry.count do
    (
        -- m_index here is dummy
        local lookupitem = yh_material_object_index_pair m_name:geometry[geoidx].material.name m_index:-1;
        local found_item = bsearch lookupitem mat_ary yh_material_object_index_pair_name_comp;
        print (format "found %, %\n" found_item.m_index found_item.m_name)

        -- error check
        if found_item.m_index > 0 then (
            append mat_obj_ary[found_item.m_index] geometry[geoidx]
        )
        else (
            print (format "Error! object % (%) is not found. No shader assigned?" \
                     geoidx lookupitem.m_name)
        )

        -- progress report
        if (mod geoidx percent_count) == 0 then (
            print (format "Prog: % percent done. " (geoidx / percent_count))
        )
    )

    return mat_obj_ary
)

--
-- Check the consistency of material object map array
--
function yh_check_consistency_material_object_map mat_obj_ary =
(
    is_ok = true

    for i = 1 to sceneMaterials.count  do
    (
        local mat_name = sceneMaterials[i].name;
        for j = 1 to mat_obj_ary[i].count do
        (
            if (mat_obj_ary[i][j].material.name != mat_name) then (
                is_ok = false
                print (format "Error! inconsistent material name.")
            )
        )
        print (format "Verified % material." i)
    )

    return is_ok
)


--
-- test main function. also example of how to use this script.
--
function yh_test_check_material_object_map =
(
    -- get mat_ary: array of { material name, material index } ,
    local mat_ary     = yh_collect_material();

    -- get mat_obj_array: mat_obj_array[material_index][index_of_geometry_of_the_same_materias]
    -- sceneMaterials[material_index] gives material
    local mat_obj_ary = yh_create_material_object_array mat_ary;

    print (format "material count = %. " mat_ary.count)
    local total_geom = 0
    for i = 1 to mat_ary.count  do
    (
        total_geom = total_geom + mat_obj_ary[i].count
    )
    print (format "total geom = %, geom.count = %.  "\
           total_geom geometry.count)

    -- Check the consistency
    is_consistent = (yh_check_consistency_material_object_map mat_obj_ary)
    if is_consistent == true then (
        print (format "material object array is consistent. ")
    )
    else (
        print (format "Error! material object array is not consistent. ")
    )
)

--
-- test main function
--
function yh_test_material_object_map_main =
(
    --disableSceneRedraw()
    --setWaitCursor()

    local t_start = 1.0 * timestamp()

    yh_test_check_material_object_map ()

    local total_time =(timestamp() - t_start)
    print (format "Elapsed time %ms\n" total_time)

    setArrowCursor()
    enableSceneRedraw()
    completeredraw()
)


-- If you test this script, uncomment this and run.
-- yh_test_material_object_map_main()
