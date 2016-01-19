from django.shortcuts import render
from collections import OrderedDict
from .models import Snugget, Location, SiteSettings



def app_view(request):
    location = Location.get_solo()
    settings = SiteSettings.get_solo()
    template = "no_content_found.html"

    # if user submitted lat/lng, find our snuggets and send them to our template
    if 'lat' and 'lng' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']

        if len(lat) > 0:
            snugget_content = Snugget.findSnuggetsForPoint(lat=float(lat), lng=float(lng))

            data = {}
            if snugget_content is not None:
                for key, values in snugget_content['groups'].items():
                    sections = {}
                    if values:
                        template = 'found_content.html'
                        heading = values[0].heading
                        for text_snugget in values:
                            if not text_snugget.image:
                                text_snugget.dynamic_image = fire_dial_icon(text_snugget.percentage)
                            if text_snugget.section in sections:
                                sections[text_snugget.section].append(text_snugget)
                            else:
                                sections[text_snugget.section] = [text_snugget]

                        data[key] = {
                            'heading': heading,
                            'sections': sections
                        }

        return render(request, template, {
            'location': location,
            'settings': settings,
            'data': OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        })


    # if not, we'll still serve up the same template without data
    else:
        return render(request, 'index.html', {
            'location': location,
            'settings': settings
            })


def fire_dial_icon(percentage):
    return """<svg
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:cc="http://creativecommons.org/ns#"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
       xmlns:svg="http://www.w3.org/2000/svg"
       xmlns="http://www.w3.org/2000/svg"
       width="100px"
       height="50px"
       viewBox="0 0 354.00001 179.16412"
       id="svg4816"
       version="1.1">
      <defs
         id="defs4818">

    <!-- the arrowhead -->
        <marker
           orient="auto"
           refY="0"
           refX="0"
           id="marker9645"
           style="overflow:visible">
          <path
             id="path9647"
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
           style="stroke:#2c2c2c;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
           id="path5986"
           class="low-color"
           d="M 107.19339,423.43023 A 175,175 0 0 1 140.61542,320.56782 L 282.19339,423.43024 Z" />

    <!-- middle-left segment -->
        <path
           d="m 140.90018,320.39188 a 175,175 0 0 1 87.49999,-63.57247 l 54.07798,166.43489 z"
           id="path5984"
           class="moderate-color"
           style="stroke:#000000;stroke-width:1;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none" />

    <!-- middle segment -->
        <path
           d="m 228.23974,256.69096 a 175,175 0 0 1 108.15594,0 l -54.07796,166.43489 z"
           id="path5994"
           class="high-color"
           style="stroke:#2c2c2c;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />

    <!-- middle-right segment -->
        <path
           style="stroke:#2c2c2c;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
           id="path5992"
           class="very-high-color"
           d="m 336.45822,256.70085 a 175,175 0 0 1 87.50001,63.57248 L 282.38025,423.13574 Z" />

    <!-- rightmost segment -->
        <path
           style="stroke:#000000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none"
           id="path5274"
           class="extreme-color"
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
           style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:4.00000024;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none;marker-end:url(#marker9645)"
           d="M 282.4,420.6 448.2,420.6"
           id="path7305" />

    <!-- this path is the outline -->
        <path
           d="m 107.07684,422.57976 a 175,175 0 0 1 175.00001,-174.99999 175,175 0 0 1 174.99999,175 l -175,0 z"
           id="path5990"
           style="fill:#000000;fill-opacity:0;stroke:#2c2c2c;stroke-width:4;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />


    <!-- this path is the centre point that the arrow comes out of -->
        <path
           style="fill:#2c2c2c;fill-opacity:1;stroke:#2c2c2c;stroke-width:4;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
           id="path4870"
           d="m 264.12235,422.00333 a 18.15621,18.15621 0 0 1 18.15621,-18.15621 18.15621,18.15621 0 0 1 18.15621,18.15621 l -18.15621,0 z" />

      </g>
    </svg>"""
