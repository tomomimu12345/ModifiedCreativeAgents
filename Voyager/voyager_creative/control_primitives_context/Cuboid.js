async function placeCuboid(bot, name, start, end, isHollow) {
    const positions = await getCuboidVoxels(start, end, isHollow);
  
    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
  }