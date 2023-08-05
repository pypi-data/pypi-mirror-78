from pyjou import root

jou = root()
jou.file.read_case.set(
	path = 'cas/case.cas')
jou.file.read_journal.set(
	path = ['jou-1.jou', 'jou-2.jou'])
jou.file.mesh_replace.set(
	path = 'msh/mesh.msh')
jou.file.write_case.set(
	path = 'cas/new.cas')
jou.file.write_case_data.set(
	path = 'cas/new-cas-dat.cas')
jou.define.boundary_conditions.velocity_inlet.set(
	name = 'inlet', velocity = 10, temperature = 300)
jou.define.boundary_conditions.pressure_outlet.set(
	name = 'outlet', temperature = 300)
jou.define.boundary_conditions.wall.set(
	name = 'wall-1', temperature = 1000)
jou.define.models.viscous.set(
	model = 'kw-sst')
jou.surface.line_surface.set(
	name = 'line-1', x1 = 0, x2 = 0, y1 = 0, y2 = .005)
jou.surface.point_surface.set(
	name = 'pt-1', x = 0, y = 2)
jou.mesh.translate.set(
	x = 10, y = 0)
jou.mesh.modify_zones.append_mesh.set(
	path = 'msh/new-msh.msh')
jou.mesh.modify_zones.merge_zones.set(
	list_zones = ['one-zone', 'another-zone'])
jou.mesh.modify_zones.fuse_face_zones.set(
	list_zones = ['one-zone', 'another-zone'])
jou.mesh.modify_zones.zone_name.set(
	old_name = 'old', new_name = 'new')
jou.mesh.check.set()
jou.mesh.repair_improve.repair.set()
jou.solve.monitors.residual.convergence_criteria.set(
	criteria = [1e-6, 1e-6, 1e-6, 1e-6, 1e-6, 1e-6])
jou.solve.initialize.initialize_flow.set()
jou.solve.initialize.compute_defaults.velocity_inlet.set(
	name = 'inlet')
jou.solve.iterate.set(
	iters = 1e3)
jou.report.fluxes.mass_flow.set(
	path = 'out/out.txt')
jou.report.fluxes.heat_transfer.set(
	path = 'out/out.txt', all_zones = False, list_zones = 'one-zone')
jou.report.surface_integrals.area.set(
	path = 'out/out.txt', list_zones = ['one-zone', 'another-zone'])
jou.report.surface_integrals.facet_avg.set(
	path = 'out/out.txt', value = 'velocity', list_zones = ['axis'])
jou.save('worked.jou')