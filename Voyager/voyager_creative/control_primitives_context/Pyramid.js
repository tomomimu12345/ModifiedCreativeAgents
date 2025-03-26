async function placePyramid(bot, name, center, baseSize, height, isHollow) {
    const positions = await getPyramidVoxels(center, baseSize, height, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}