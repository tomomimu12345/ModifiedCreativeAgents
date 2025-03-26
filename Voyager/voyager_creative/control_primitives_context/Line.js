async function placeLine(bot, BlockName, start, end) {
  const positions = await getLineVoxels(start, end);

  for (const pos of positions) {
      await placeItem(bot, BlockName, pos);
  }
}