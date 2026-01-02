#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>

// C++ Simple Ray Tracer
// Generates a PPM image file

struct Vec3 {
    double x, y, z;
    Vec3(double x=0, double y=0, double z=0) : x(x), y(y), z(z) {}
    Vec3 operator+(const Vec3& v) const { return Vec3(x+v.x, y+v.y, z+v.z); }
    Vec3 operator-(const Vec3& v) const { return Vec3(x-v.x, y-v.y, z-v.z); }
    Vec3 operator*(double d) const { return Vec3(x*d, y*d, z*d); }
    double dot(const Vec3& v) const { return x*v.x + y*v.y + z*v.z; }
    Vec3 normalize() const {
        double mg = std::sqrt(x*x + y*y + z*z);
        return Vec3(x/mg, y/mg, z/mg);
    }
};

int main() {
    const int width = 400;
    const int height = 300;
    
    std::ofstream img("output.ppm");
    img << "P3\n" << width << " " << height << "\n255\n";
    
    Vec3 spherePos(0, 0, -5);
    double radius = 1.0;
    
    std::cout << "Rendering Trace to 'output.ppm'..." << std::endl;
    
    for (int y = height-1; y >= 0; y--) {
        for (int x = 0; x < width; x++) {
            // Ray Trace Logic
            double u = (double)x / width;
            double v = (double)y / height;
            
            // Screen coords (-1 to 1)
            Vec3 rayDir(u*4.0 - 2.0, v*3.0 - 1.5, -1.0);
            rayDir = rayDir.normalize();
            Vec3 rayOrigin(0, 0, 0);
            
            // Sphere Intersection
            Vec3 oc = rayOrigin - spherePos;
            double a = rayDir.dot(rayDir);
            double b = 2.0 * oc.dot(rayDir);
            double c = oc.dot(oc) - radius*radius;
            double discriminant = b*b - 4*a*c;
            
            int ir, ig, ib;
            
            if (discriminant > 0) {
                // Hit Sphere (Red)
                ir = 255; ig = 0; ib = 0;
            } else {
                // Background (Gradient Blue)
                double t = 0.5 * (rayDir.y + 1.0);
                ir = (int)(255 * (1.0 - t) + 128 * t);
                ig = (int)(255 * (1.0 - t) + 178 * t);
                ib = (int)(255 * (1.0 - t) + 255 * t);
            }
            
            img << ir << " " << ig << " " << ib << "\n";
        }
    }
    
    std::cout << "Done!" << std::endl;
    return 0;
}
