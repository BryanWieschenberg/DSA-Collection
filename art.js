import net from "net";

const checkPort = (port) => {
    return new Promise((resolve) => {
        const socket = net.connect(port, "127.0.0.1", () => {
            socket.end();
            resolve(true);
        });
        socket.on("error", () => {
            resolve(false);
        });
        socket.setTimeout(250);
        socket.on("timeout", () => {
            socket.destroy();
            resolve(false);
        });
    });
};

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
    await wait(500);
    let attempts = 0;
    const maxAttempts = 240;
    while (attempts < maxAttempts) {
        const apiReady = await checkPort(8000);
        const webReady =
            (await checkPort(5173)) ||
            (await checkPort(4173)) ||
            (await checkPort(5174));

        if (apiReady && webReady) {
            console.log(
                "\x1b[32m" +
                    `              _____________    ____________    ____________            _______          __________        ___________       __
             /   _________/   |   _________|  |____    ____|          /____   \\       /    ____   \\      |   _______ \\     |  |
            /   /             |  |                 |  |                    |   |     /    /    \\   \\     |  |       \\ \\    |  |
           /   /              |  |                 |  |                    |   |    /    /      \\   \\    |  |        \\ \\   |  |
          /   /               |  |                 |  |                    |   |   |    |        |   |   |  |        / /   |  |
         /   /      _____     |  |______           |  |                    |   |   |    |        |   |   |  |_______/ /    |  |
        |   |      /___  \\    |   ______|          |  |                    |   |   |    |        |   |   |   _______ /     |  |
        |   |          |  |   |  |                 |  |              __    |   |   |    |        |   |   |  |       \\ \\    |  |
        |   |          |  |   |  |                 |  |             |  |   |   |   |    |        |   |   |  |        \\ \\   |  |
        |   |          |  |   |  |                 |  |             |  |   |   |    \\    \\      /   /    |  |        / /   |__|
        |    \\_________|  |   |  |_________        |  |             |  |___|   |     \\    \\____/   /     |  |_______/ /     __
         \\                |   |            |       |  |             |          |      \\           /      |           /     /  \\
          \\______________/    |____________|       |__|              \\________/        \\_________/       |__________/      \\__/` +
                    "\x1b[0m",
            );
            process.exit(0);
        }
        attempts++;
        await wait(250);
    }
    process.exit(0);
}

main();
