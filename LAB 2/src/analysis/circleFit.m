% This function calculates the best fit circle for a distribution and gives
% the rms error of the dataset from the circle. 
function [x,y,r,errorRMS] = circleFit(circle_E, circle_N)
   len = length(circle_E);
   One = ones([len,1]);
   A = [circle_E, circle_N, One];
   B = zeros(len,1);
   for i = 1:len
       v = [circle_E(i),circle_N(i)];
       B(i) = circle_E(i)^2 + circle_N(i)^2;
   end
   X = pinv(A)*B;
   x = X(1)/2;
   y = X(2)/2;
   r = ((4*X(3)+ X(2)^2 + X(1)^2)^0.5)/2;

circ = length(circle_E);
error = zeros(circ,1);
for i = 1:circ
    v = [circle_E(i)-x,circle_N(i)-y];
    dist = norm(v);
    error(i) = dist-r;
end
errorRMS = rms(error);
end
