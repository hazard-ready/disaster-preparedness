from math import sin, cos, radians
from random import randint

dial = """<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="105px"
   height="65px"
   viewBox="0 0 354.00001 179.16412"
   version="1.1">
  <defs>

<!-- the arrowhead -->
    <marker
       orient="auto"
       refY="0"
       refX="0"
       id="arrowhead-{2}"
       style="overflow:visible">
      <path
         style="fill:#000000;fill-opacity:1;fill-rule:evenodd;stroke:#000000;stroke-width:0.625;stroke-linejoin:round;stroke-opacity:1"
         d="M 8.7185878,4.0337352 -2.2072895,0.01601326 8.7185884,-4.0017078 c -1.7454984,2.3720609 -1.7354408,5.6174519 -6e-7,8.035443 z"
         transform="matrix(-1.1,0,0,-1.1,-1.1,0)" />
    </marker>
  </defs>
  <metadata
     id="metadata4821">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     id="layer1"
     transform="translate(-105.07686,-245.57977)">

<!-- leftmost segment -->
    <path
       class="intensity-meter-segment low-color"
       d="M 107.19339,423.43023 A 175,175 0 0 1 140.61542,320.56782 L 282.19339,423.43024 Z" />

<!-- middle-left segment -->
    <path
        class="intensity-meter-segment moderate-color"
        d="m 140.90018,320.39188 a 175,175 0 0 1 87.49999,-63.57247 l 54.07798,166.43489 z" />

<!-- middle segment -->
    <path
        class="intensity-meter-segment high-color"
        d="m 228.23974,256.69096 a 175,175 0 0 1 108.15594,0 l -54.07796,166.43489 z" />

<!-- middle-right segment -->
    <path
       class="intensity-meter-segment very-high-color"
       d="m 336.45822,256.70085 a 175,175 0 0 1 87.50001,63.57248 L 282.38025,423.13574 Z" />

<!-- rightmost segment -->
    <path
       class="intensity-meter-segment extreme-color"
       d="m 423.99891,320.28102 a 175,175 0 0 1 33.42202,102.86241 l -175,0 z" />


<!-- this path is the arrow -->
<!-- in the d attribute:
d="M originX originY headX headY"
0,0 is up and left of the viewbox
Y=256.2 is lined up with the inside-top of the dial
Y=420.6 is lined up with the inside-bottom
So the length of the arrow must have to be 164.4 pixels
X=282.4 is the centre
X=118 is lined up with the inside-left
X=448.2 is lined up with the inside-right
This gives a length range from 164.4 to 165.8.  Hrm....
-->
    <path
       style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:4.00000024;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none;marker-end:url(#arrowhead-{2})"
       d="M 282.4,420.6 {0}, {1}"/>

<!-- this path is the outline -->
    <path
       d="m 107.07684,422.57976 a 175,175 0 0 1 175.00001,-174.99999 175,175 0 0 1 174.99999,175 l -175,0 z"
       style="fill:#000000;fill-opacity:0;stroke:#2c2c2c;stroke-width:4;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />


<!-- this path is the centre point that the arrow comes out of -->
    <path
       style="fill:#2c2c2c;fill-opacity:1;stroke:#2c2c2c;stroke-width:4;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="m 264.12235,422.00333 a 18.15621,18.15621 0 0 1 18.15621,-18.15621 18.15621,18.15621 0 0 1 18.15621,18.15621 l -18.15621,0 z" />

  </g>
</svg>"""

def make_icon(percentage):
    if not percentage:
        return None

    # Percentages are given like '42' in the snuggets, so make them percentages of 1.
    # Our fire dial spans 180 degrees, and 0 on it is at 180 in a polar coordinate system.
    # Also, python's trig functions work in radians.
    theta = radians(180 - (percentage * 0.01 * 180))
    r = 165 # the length of the arrow

    # Get x and y, which are the distances from the fire dial, with its center as 0,0
    x = r * cos(theta)
    y = r * sin(theta)

    # The center of the fire dial, in svg coordinates, which start from the top left.
    y_center = 420.6
    x_center = 282.4

    # Put x and y in the svg coordinate space
    transform_x = x_center + x
    transform_y = y_center - y

    # Look for {0} and {1} above to see where the arrow path goes.
    # The third argument is a salt for the marker element IDs, which must be unique per page.
    return dial.format(transform_x, transform_y, randint(0, 9999))
