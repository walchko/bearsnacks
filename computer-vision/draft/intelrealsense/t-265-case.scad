$fn=90;

module camera(){
    difference()
    {
        cube([78,27,8]);
        translate([15,8.5,-1]) cylinder(h=15,d=3);
        translate([70, 8.5,-1]) cylinder(h=15,d=3);
        translate([-1,5,-1]) cube([2,22-5, 10]);
    }
    color("gray") translate([28,9,0]) cylinder(h=9, d=6);
    color("gray") translate([58.5,9,0]) cylinder(h=9, d=6);

    color("silver") translate([37,18,0]) cube([51-37,8, 9]);
}

module bread_board(){
    difference()
    {
        color("blue") cube([46, 35, 10]);
        translate([5,35/2,-1]) cylinder(h=15,d=2.1);
        translate([41, 35/2,-1]) cylinder(h=15,d=2.1);
    }
}

module base(w,l,h, r){
    translate([r,r,0]) minkowski()
    {
      cube([w-2*r,l-2*r,h-1]);
      cylinder(r=r,h=1);
    }
}

module qwiic(){
    /* color("green") base(25.4, 17.78, 2,2); */
    color("green") base(17.78, 25.4, 2,2);
    // cube([25.4, 17.78,1]);
}

r = 5;
l = 100;
w = 75;
h = 35;

difference(){
    base(l,w,h,r);
    translate([-1,r,4]) cube([l+5,w-2*r,h]);
}

translate([l-78-1, r+1, 10]) camera();
translate([l-46-1, w-35-r-1, 4]) bread_board();
translate([5, w-30-r-1, 8]) qwiic();
translate([5, w-30-r-1, 8+7]) qwiic();
translate([5, w-30-r-1, 8+14]) qwiic();
