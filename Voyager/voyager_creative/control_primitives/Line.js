async function getLineVoxels(start, end) {
    const positions = [];
    const dx = Math.abs(end.x - start.x);
    const dy = Math.abs(end.y - start.y);
    const dz = Math.abs(end.z - start.z);
  
    const sx = start.x < end.x ? 1 : -1;
    const sy = start.y < end.y ? 1 : -1;
    const sz = start.z < end.z ? 1 : -1;
  
    let err1, err2;
    if (dx >= dy && dx >= dz) {
      err1 = 2 * dy - dx;
      err2 = 2 * dz - dx;
      let y = start.y, z = start.z;
      for (let x = start.x; x !== end.x + sx; x += sx) {
        positions.push(new Vec3(x, y, z));
        if (err1 > 0) {
          y += sy;
          err1 -= 2 * dx;
        }
        if (err2 > 0) {
          z += sz;
          err2 -= 2 * dx;
        }
        err1 += 2 * dy;
        err2 += 2 * dz;
      }
    } else if (dy >= dx && dy >= dz) {
      err1 = 2 * dx - dy;
      err2 = 2 * dz - dy;
      let x = start.x, z = start.z;
      for (let y = start.y; y !== end.y + sy; y += sy) {
        positions.push(new Vec3(x, y, z));
        if (err1 > 0) {
          x += sx;
          err1 -= 2 * dy;
        }
        if (err2 > 0) {
          z += sz;
          err2 -= 2 * dy;
        }
        err1 += 2 * dx;
        err2 += 2 * dz;
      }
    } else {
      err1 = 2 * dx - dz;
      err2 = 2 * dy - dz;
      let x = start.x, y = start.y;
      for (let z = start.z; z !== end.z + sz; z += sz) {
        positions.push(new Vec3(x, y, z));
        if (err1 > 0) {
          x += sx;
          err1 -= 2 * dz;
        }
        if (err2 > 0) {
          y += sy;
          err2 -= 2 * dz;
        }
        err1 += 2 * dx;
        err2 += 2 * dy;
      }
    }
  
    return positions;
}
  

async function placeLine(bot, BlockName, start, end) {
    const positions = await getLineVoxels(start, end);

    for (const pos of positions) {
        await placeItem(bot, BlockName, pos);
    }
}