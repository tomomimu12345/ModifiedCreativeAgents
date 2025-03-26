async function placeSphere(bot, name, center, radius, isHollow) {
    const positions = await getSphereVoxels(center, radius, isHollow);

    for (const pos of positions) {
        await placeItem(bot, name, pos);
    }
}