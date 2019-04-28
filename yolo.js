// Copyright (c) 2018 ml5
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

let yolo_video;
let yolo;
let yolo_status;
let objects = [];

function setup() {
  let height = 640;
  let width = 480;

  createCanvas(height, width);
  yolo_video = createCapture(yolo_video);
  yolo_video.size(height, width);

  // Create a YOLO method
  yolo = ml5.YOLO(yolo_video, startDetecting);

  // Hide the original yolo_video
  yolo_video.hide();
  yolo_status = select('#yolo_status');
}

function draw() {
  image(yolo_video, 0, 0, width, height);
  for (let i = 0; i < objects.length; i++) {
    noStroke();
    fill(0, 255, 0);
    text(objects[i].className, objects[i].x * width, objects[i].y * height - 5);
    noFill();
    strokeWeight(4);
    stroke(0, 255, 0);
    rect(objects[i].x * width, objects[i].y * height, objects[i].w * width, objects[i].h * height);
  }
}

function startDetecting() {
  yolo_status.html('Model loaded!');
  detect();
}

function detect() {
  yolo.detect(function(err, results) {
    objects = results;
    detect();
  });
}
