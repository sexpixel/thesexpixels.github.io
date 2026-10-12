# CV page 2: (stage number, stage name, [(discipline, [points], credits), ...]). Edit here, then run build.py.
stages=[
 ('00','Across the whole show',[
  ('Production methodologies',['Feature film supervision','Episodic / streaming supervision','Commercial / advertising supervision','Animation feature supervision','Virtual production / LED stage'],'Panda Plan · Gangs of London S3 · Black Sails S4'),
  ('Pipeline & tools',['Custom gizmos and NDK plugins','Python / TCL development','Nuke script templating','AYON and Deadline','RV and Syncsketch'],'Unreal Fellowship, Epic Games'),
  ('Client & creative leadership',['Dailies leadership','Sequence continuity','Final shot sign-off','Mentoring artists and comp leads','Client review'],'Game of Thrones S6 · Man in an Orange Shirt')]),
 ('01','Plan & shoot',[
  ('Pre-production & planning',['Script breakdown for VFX shots','Bid input and feasibility','Methodology definition','Previz, postviz and techviz direction'],'Framestore FPS, Lead PostVis · Playmaker'),
  ('On-set supervision',['On-set decision making','Director and DP liaison','HDRI, chrome and grey ball capture','LIDAR','Witness camera arrays'],'The Ballad of a Small Player, dir. Edward Berger'),
  ('3D & USD',['Photo-modelling and scan geometry','Nuke 3D camera projection','USD scene assembly','AI image-to-geometry'],'Hugo · BBC World Cup titles · NukeGeoTools')]),
 ('02','Clean the plate',[
  ('Prep & cleanup',['Rig, wire and marker removal','Crew, boom and reflection removal','Sign, logo and text removal','Beauty work'],'Damsel · Poldark S5'),
  ('Roto & segmentation',['Hero character isolation','Fine-detail and hair roto','Garbage and holdout mattes','AI-assisted segmentation and matte QA'],'The Ballad of a Small Player'),
  ('AI & agentic coding',['Agentic coding for all tool development','Diffusion model compositing','AI roto and matte QA','Cross-model verification'],'ComfyUI · NukeGeoTools · Playmaker app')]),
 ('03','Solve the plate',[
  ('Tracking & matchmove',['3D camera tracking','2D and point tracking','Object tracking','SmartVector'],'Gangs of London S3 · The Rig'),
  ('Keying & extraction',['Blue and green screen keying','Core / edge matte separation','Despill','Hair and fur preservation'],'The Crown S2 · Captain Marvel'),
  ('Plate reconstruction',['Clean plate generation','Patch, rebuild and restoration','Multi-frame reconstruction','Projection-based repair'],'The Ballad of a Small Player')]),
 ('04','Build the shot',[
  ('Environments & DMP',['Set extensions','Projection mapping (3D / 2.5D)','Matte painting integration','Sky replacements'],'The Buccaneers · Great Expectations'),
  ('CG & AOV integration',['Multi-pass assembly','AOV rebuilds','Creature and vehicle integration','Re-lighting in Nuke'],'Guardians of the Galaxy · Captain Marvel'),
  ('Deep compositing',['Deep compositing and multi-depth layers','Deep holdouts and merges','Depth-ordered atmospherics'],'Walking With Dinosaurs')]),
 ('05','Shape the look',[
  ('Camera & lens work',['Bokeh and defocus','Flare matching','Lens distortion / undistortion','STMap reprojection'],'Tenet · The French Dispatch'),
  ('FX element integration',['FX simulation pass comp','Practical fire, smoke and sparks','Muzzle flashes and explosions'],'Black Sails S4 · Lost in Space S2'),
  ('Creative & experimental FX',['Time warping and echo effects','Procedural comp FX via gizmos','Stylised and non-photoreal looks','Music video and promo FX'],"Klaxons 'Twin Flames' UKMVA · M.I.A. 'Borders' · Coldplay 'Daddy'")]),
 ('06','Finish & deliver',[
  ('Lookdev & shot finishing',['ACES / OCIO','Colour matching and balancing','Day-for-night','Grain matching and regrain'],'Yardie · Murder Is Easy'),
  ('Stereo & immersive',['Mono-to-stereo conversion','Stereo eye matching','Depth maps','360 comp passes'],'Hugo · Save The 365th Day'),
  ('Delivery, reels & submissions',['Editorial turnovers and change lists','EDL / AAF conform and VFX pulls','DCP production','Oscar and BAFTA submission prep'],'Absolute Post, deliveries across eight shows')]),
]

def header(current=''):
    def cur(k): return ' aria-current="page"' if k==current else ''
    return f'''<header class="nav" id="nav">
  <a class="mark" href="/" aria-label="Mark Pinheiro, VFX Supervisor, home"><b>Mark Pinheiro</b><small>VFX Supervisor</small></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <nav aria-label="Main" id="menu">
    <ul>
      <!-- Showreels. When a reel exists, give its link href="<video url>" data-video="vimeo:ID:HASH", like Nuke Compositor. -->
      <li><a href="/#reel-filmmaker">Filmmaker</a></li>
      <li><a href="https://vimeo.com/1232958213/ffbea294d7" data-video="vimeo:1232958213:ffbea294d7">Nuke Compositor</a></li>
      <li><a href="/#reel-vfx-supervisor">VFX Supervisor</a></li>
      <li><a href="/skills/"{cur('skills')}>Skills</a></li>
      <li class="sep" aria-hidden="true"></li>
      <li><a href="/#work">Work</a></li>
      <li><a href="/about/"{cur('about')}>About</a></li>
      <li><a href="/#contact">Contact</a></li>
    </ul>
  </nav>
</header>'''

