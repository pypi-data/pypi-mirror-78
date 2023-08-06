if( USE_PYBIND )

	add_library(pybind11_interface SHARED MultiScaleOT_pybind11_interface.cpp)

	target_compile_options(pybind11_interface PUBLIC ${PYBIND_COMPILE_OPTIONS})
	
	target_link_libraries(pybind11_interface
		Common
		)
		
	if ( USE_SINKHORN )
		target_link_libraries(pybind11_interface
			Sinkhorn
			)
	endif ( USE_SINKHORN)
	
	set_target_properties(pybind11_interface PROPERTIES PREFIX "")
	set_target_properties(pybind11_interface PROPERTIES SUFFIX ${PYTHON_EXTENSION_SUFFIX})
	set_target_properties(pybind11_interface PROPERTIES OUTPUT_NAME MultiScaleOT)


endif( USE_PYBIND )
