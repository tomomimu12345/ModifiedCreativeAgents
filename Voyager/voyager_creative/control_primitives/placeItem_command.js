const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function placeItem(bot, name, position) {
    // return if name is not string
    if (typeof name !== "string") {
        throw new Error(`name for placeItem must be a string`);
    }
    // return if position is not Vec3
    if (!(position instanceof Vec3)) {
        throw new Error(`position for placeItem must be a Vec3`);
    }
    const itemByName = mcData.itemsByName[name];
    if (!itemByName) {
        throw new Error(`No item named ${name}`);
    }

    x = Math.round(position.x)
    y = Math.round(position.y)
    z = Math.round(position.z)

    bot.chat(`/setblock ${x} ${y} ${z} ${name}`)
    // bot.save(`${name}_placed`);
    bot.emit("blockPlace", position);
    await delay(1);
}
