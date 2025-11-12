#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoords;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform vec3 objectColor;
uniform float time;

void main()
{
    // Water-specific lighting
    float ambientStrength = 0.3;
    vec3 ambient = ambientStrength * lightColor;
    
    // Diffuse with wave effects
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    
    // Add specular highlights for water shine
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 128.0);
    vec3 specular = specularStrength * spec * lightColor;
    
    // Water color with depth and time variation
    vec3 waterColor = objectColor;
    
    // Depth-based color variation
    float depth = abs(FragPos.y);
    waterColor *= (1.0 - depth * 0.5);
    
    // Time-based color variation (subtle)
    waterColor.g += sin(time * 0.3) * 0.05;
    
    // Final color calculation
    vec3 result = (ambient + diff * lightColor + specular) * waterColor;
    
    // Water transparency - more opaque for realism
    FragColor = vec4(result, 0.95);
}