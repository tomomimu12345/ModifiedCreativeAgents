async function getCuboidVoxels(start, end, isHollow) {
  const positions = [];
  const minX = Math.min(start.x, end.x);
  const maxX = Math.max(start.x, end.x);
  const minY = Math.min(start.y, end.y);
  const maxY = Math.max(start.y, end.y);
  const minZ = Math.min(start.z, end.z);
  const maxZ = Math.max(start.z, end.z);

  for (let x = minX; x <= maxX; x++) {
      for (let y = minY; y <= maxY; y++) {
      for (let z = minZ; z <= maxZ; z++) {
          if (isHollow) {
          if (x === minX || x === maxX || y === minY || y === maxY || z === minZ || z === maxZ) {
              positions.push(new Vec3(x, y, z));
          }
          } else {
          positions.push(new Vec3(x, y, z));
          }
      }
      }
  }
  return positions;
}

async function placeCuboid(bot, name, start, end, isHollow) {
  const positions = await getCuboidVoxels(start, end, isHollow);

  for (const pos of positions) {
      await placeItem(bot, name, pos);
  }
}