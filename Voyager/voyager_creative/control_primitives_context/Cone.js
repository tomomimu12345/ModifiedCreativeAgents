async function placeCone(bot, name, center, baseRadius, topRadius, height, isHollow) {
    const positions = await getConeVoxels(center, baseRadius, topRadius, height, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}