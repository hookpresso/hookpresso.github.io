(() => {
  const dot = document.querySelector('.hero-traveler');
  if (!dot || typeof dot.animate !== 'function') return;
  const svg = dot.ownerSVGElement;
  const ns = 'http://www.w3.org/2000/svg';
  const rest = [247.52, 159.84];
  const random = (min, max) => min + Math.random() * (max - min);
  const smooth = t => t * t * (3 - 2 * t);
  const rotation = 38 * Math.PI / 180;
  const ellipse = (angle, rx = 210, ry = 164) => {
    const x = rx * Math.cos(angle), y = ry * Math.sin(angle);
    return [220 + x * Math.cos(rotation) - y * Math.sin(rotation),
      220 + x * Math.sin(rotation) + y * Math.cos(rotation)];
  };
  const entry = ellipse(-Math.PI / 2);
  const bezier = (points, t) => [0, 1].map(axis =>
    (1-t)**3 * points[0][axis] + 3*(1-t)**2*t * points[1][axis]
    + 3*(1-t)*t*t * points[2][axis] + t**3 * points[3][axis]);
  const node = (tag, attributes, parent = svg) => {
    const element = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
    parent.appendChild(element);
    return element;
  };
  const portals = [0, 1].map(() => {
    const portal = node('g', {class:'wormhole', opacity:0});
    node('ellipse', {class:'wormhole-halo', rx:29, ry:17}, portal);
    node('ellipse', {class:'wormhole-ring wormhole-ring-a', rx:22, ry:12}, portal);
    node('ellipse', {class:'wormhole-ring wormhole-ring-b', rx:16, ry:21}, portal);
    node('ellipse', {class:'wormhole-ring wormhole-ring-c', rx:12, ry:7}, portal);
    node('ellipse', {class:'wormhole-core', rx:8, ry:5}, portal);
    return portal;
  });
  const trails = Array.from({length:8}, (_, i) => {
    const trail = node('circle', {class:'wormhole-trail', r:Math.max(1, 3.5-i*.3),
      fill:i<3?'#FFD60A':'#b1a0ff', opacity:0});
    svg.insertBefore(trail, dot);
    return trail;
  });
  // Keep the traveler above its wake and the portal rings.
  svg.appendChild(dot);
  let animation;
  let effects = [];

  function explore() {
    for (const effect of effects) effect.cancel();
    effects = [];
    const frames = [];
    let elapsed = 0;
    let current = rest;
    const add = (position, time, scale=1, opacity=1) => {
      current = position;
      frames.push({
        transform:`translate(${position[0]}px, ${position[1]}px) scale(${scale})`,
        opacity, time
      });
    };
    const travel = (curve, duration, size = () => 1, alpha = () => 1, easing = smooth, steps = 90) => {
      for (let i=1; i<=steps; i++) {
        const t=i/steps;
        add(curve(easing(t)), elapsed+duration*t, size(t), alpha(t));
      }
      elapsed += duration;
    };
    const exit = [random(75, 345), random(65, 105)];
    const direction = Math.random()<.5 ? -1 : 1;
    add(rest, 0);
    elapsed = random(.45, .9);
    add(rest, elapsed);
    // Collapse into the logo's tiny portal, then emerge somewhere unexpected.
    travel(t => [rest[0]+Math.sin(t*Math.PI*4)*12*(1-t),
      rest[1]+Math.cos(t*Math.PI*4)*8*Math.sin(Math.PI*t)], .8,
      t => 1-t, t => 1-t);
    add(exit, elapsed, 0, 0);
    travel(t => {
      const radius=27*t;
      const angle=direction*t*Math.PI*3;
      return [exit[0]+Math.cos(angle)*radius, exit[1]+Math.sin(angle)*radius*.6];
    }, 1.1, t => 1.5*Math.sin(t*Math.PI/2), t => Math.min(1,t*4));
    const start = current;
    travel(t => bezier([start, [random(60,380), 20], [entry[0]+45, entry[1]-25], entry],t), .75,
      t => 1.5-.5*t);
    const turns = Math.random()<.5 ? 1 : 2;
    // After the portal exit, follow a steady ellipse at a constant size.
    travel(t => ellipse(-Math.PI/2+direction*t*Math.PI*2*turns),
      random(3.2,5.2), () => 1, () => 1, t => t, 240);
    travel(t => bezier([entry,[entry[0]-65,35],[exit[0]+65,exit[1]-25],exit],t),1,
      t => 1-t, t => 1-t);
    add(rest, elapsed, 0, 0);
    travel(() => rest,.65,t => 1+Math.sin(t*Math.PI)*.65,
      t => Math.min(1,t*4));
    elapsed += random(.5,1.2);
    add(rest,elapsed);

    const keyframes=frames.map(({time,...frame})=>({...frame,offset:time/elapsed}));
    const options={duration:elapsed*1000,easing:'linear',fill:'both'};
    animation=dot.animate(keyframes,options);
    dot.style.animation='none';
    effects.push(animation);
    trails.forEach((trail,i)=>{
      const wake=keyframes.map(frame=>({...frame,opacity:frame.opacity*(.3-i*.027)}));
      effects.push(trail.animate(wake,{...options,delay:(i+1)*32}));
    });
    portals.forEach((portal,i)=>{
      const position=i===0?rest:exit;
      const transform=scale=>`translate(${position[0]}px, ${position[1]}px) scale(${scale})`;
      effects.push(portal.animate([
        {offset:0,opacity:0,transform:transform(.1)},
        {offset:.08,opacity:1,transform:transform(1)},
        {offset:.22,opacity:i===0?0:.45,transform:transform(i===0?.1:.8)},
        {offset:.7,opacity:i===0?0:.45,transform:transform(i===0?.1:.8)},
        {offset:.86,opacity:1,transform:transform(1.2)},
        {offset:1,opacity:0,transform:transform(.1)}
      ],options));
    });
    if(document.hidden) effects.forEach(effect=>effect.pause());
    animation.finished.then(explore).catch(()=>{});
  }
  explore();
  const pause=()=>effects.forEach(effect=>effect.pause());
  const resume=()=>{if(!document.hidden)effects.forEach(effect=>effect.play());};
  document.addEventListener('visibilitychange',()=>document.hidden?pause():resume());
  window.addEventListener('pagehide',pause);
  window.addEventListener('pageshow',resume);
})();
