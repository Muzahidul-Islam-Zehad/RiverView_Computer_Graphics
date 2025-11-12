#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform vec3 objectColor;
uniform sampler2D texture0;
uniform bool useTexture;

void main()
{
    if (useTexture)
    {
        FragColor = texture(texture0, TexCoords);
    }
    else
    {
        FragColor = vec4(objectColor, 1.0);
    }
}