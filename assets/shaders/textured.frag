#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoords;

uniform sampler2D texture_diffuse1;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform bool useTexture;
uniform vec3 objectColor;
uniform float time;  // Add time for day/night cycle

void main()
{
    // Golden hour lighting - warm colors
    vec3 goldenLight = vec3(1.0, 0.8, 0.6);  // Warm orange-yellow light
    
    // Ambient - slightly warmer for golden hour
    float ambientStrength = 0.4;
    vec3 ambient = ambientStrength * goldenLight;
    
    // Diffuse
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * goldenLight;
    
    // Specular - softer for golden hour
    float specularStrength = 0.3;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * goldenLight;
    
    vec3 result;
    if(useTexture) {
        vec4 textureColor = texture(texture_diffuse1, TexCoords);
        // Warm up textures for golden hour
        textureColor.rgb *= vec3(1.1, 1.0, 0.9);  // Boost red, reduce blue
        result = (ambient + diffuse + specular) * textureColor.rgb;
    } else {
        // Warm up object colors for golden hour
        vec3 warmColor = objectColor * vec3(1.1, 1.0, 0.9);
        result = (ambient + diffuse + specular) * warmColor;
    }
    
    FragColor = vec4(result, 1.0);
}