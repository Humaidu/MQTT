var mqtt=require('mqtt');
// Create a client connection
var client = mqtt.connect("mqtt://mqtt.dioty.co:1883", {
username: "larteyjoshua@gmail.com",
password: "7f8a9110"
});

client.on('connect', function() { // Check you have a connection

// Subscribe to a Topic
client.subscribe("/larteyjoshua@gmail.com/test", function() {
// When a message arrives, write it to the console
        client.on('message', function(topic, message, packet) {
            console.log("Received '" + message + "' on '" + topic + "'");
        });
    });

// Publish a message to a Topic
    client.publish("/larteyjoshua@gmail.com/test", 'Hello World Message!', function() {
        console.log("Message posted...");
        client.end(); // Close the connection after publish
    });
});