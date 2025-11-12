#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D texture_diffuse1;
uniform bool useTexture;

void main()
{
    if(useTexture) {
        // Just show the texture directly, no lighting
        FragColor = texture(texture_diffuse1, TexCoords);
        
        // If texture is black, show red for debugging
        if(FragColor.r < 0.1 && FragColor.g < 0.1 && FragColor.b < 0.1) {
            FragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }
    } else {
        // Show blue if no texture
        FragColor = vec4(0.0, 0.0, 1.0, 1.0);
    }
}