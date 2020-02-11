# Altarpiece
CS 6476 Computer Vision Project

## Problem Statement

Given an image of a simulated 3D cube with an applied texture, determine its orientation and position. From the position and orientation information, extract the textures on the faces, and create a 2D net of the texture map.

## Approach

- Corners of the shape will be identified with Harris corner detection and Canny edge detection
- Orientation and position will be inferred using the Hough transform
- From the orientation and position, apply a Homography matrix to each of the visible faces to extract their texture as a 2D net
- The texture nets can be combined to create a partial texture map of the cube’s faces

## Experiments and Results

### Dataset

- The dataset of 3D renders will be generated using Blender and artificial noise will be added with various methods
- Standard Blender textures will be used for texture maps

### Experiments

- Accuracy of corner detection
  - Compare the output of our corner detection process with exact corner locations from Blender
  - This experiment will show how accurate our corner detection process is, and how robust it is to noise and variance in textures
  - Metrics: Corner distance and orientation distance
- Accuracy of texture extraction
  - Compare the output of our texture extraction process with exact texture maps from Blender
  - This experiment will show how accurate our texture extraction is, and how robust it is to noise and differing textures
  - Metrics: SSD or another more robust metric between extracted and actual textures


## Possible Extensions

- Add different shapes, such as spheres, boxes, cones and cylinders, and have our algorithm identify which object it is and apply a different texture extraction process for each possible object type
- Take multiple images of the same object from different orientations, and combine the different texture maps into a single texture map using image stitching techniques

## Video Demonstration
[Video](https://youtu.be/NAcbie5V8XM)
