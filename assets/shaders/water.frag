#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoords;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform float time;

void main()
{
    // Beautiful water blue color
    vec3 waterBaseColor = vec3(0.1, 0.6, 0.95); // Deep blue-cyan
    
    // Ambient light
    float ambient = 0.5;
    
    // Diffuse lighting
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diffuse = max(dot(norm, lightDir), 0.0) * 0.6;
    
    // Specular highlights for water reflections
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float specular = pow(max(dot(viewDir, reflectDir), 0.0), 64.0) * 0.8;
    
    // Add subtle wave animation to color
    float wave_effect = sin(TexCoords.x * 3.0 + time * 0.5) * 0.05;
    
    // Combine all effects
    vec3 result = waterBaseColor * (ambient + diffuse) + lightColor * specular;
    result += wave_effect * 0.1;
    
    FragColor = vec4(result, 0.85);  // Slightly transparent water
}