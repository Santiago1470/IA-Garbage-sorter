const http = require("http");
const PORT = 3001;


const { Board, Servo } = require("johnny-five");
const board = new Board({ port: "COM7" });

board.on("ready", () => {


    const server = http.createServer(async (req, res) => {

        // if (req.url === "/close" && req.method === "GET") {
        //     res.writeHead(200, { "Content-Type": "application/json" });
        //     const response = { message: "estoy en el motor, 0" };
        //     res.end(JSON.stringify(response));
        
        //     const servo = new Servo({
        //         pin: 7,
        //         startAt: 10,
        //     });
            
        //     servo.to(65);
        //     board.wait(1000, function () {

        //     });
        // }
        if (req.url === "/open" && req.method === "GET") {
            res.writeHead(200, { "Content-Type": "application/json" });
            const response = { message: "estoy en el motor, 1" };
            res.end(JSON.stringify(response));
        
            const servo = new Servo({
                pin: 7,
                startAt: 10,
            });
        
            servo.to(180);
            board.wait(10000, function () {
                servo.to(65);
            });
        }
        else {
            res.writeHead(404, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ message: "Route not found" }));
        }
    });

    server.listen(PORT, () => {
        console.log('server started on port: ${PORT}');
    });
});

