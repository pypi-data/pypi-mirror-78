

python gwemopt_plot_skymap -s ../data/S200115j/LALInference.fits.gz --fields ../data/S200115j/ZTF_fields.dat,../data/S200115j/TCA_fields.dat,../data/S200115j/TCH_fields.dat,../data/S200115j/TRE_fields.dat -o ../output/S200115j_0p5 -t ZTF,TCA,TCH,TRE -g 1263097398 --tmax 0.5

python gwemopt_plot_skymap -s ../data/S200115j/LALInference.fits.gz --fields ../data/S200115j/ZTF_fields.dat,../data/S200115j/TCA_fields.dat,../data/S200115j/TCH_fields.dat,../data/S200115j/TRE_fields.dat -o ../output/S200115j_1p0 -t ZTF,TCA,TCH,TRE -g 1263097398 --tmax 1.0

python gwemopt_plot_skymap -s ../data/S200115j/LALInference.fits.gz --fields ../data/S200115j/ZTF_fields.dat,../data/S200115j/TCA_fields.dat,../data/S200115j/TCH_fields.dat,../data/S200115j/TRE_fields.dat -o ../output/S200115j_2p0 -t ZTF,TCA,TCH,TRE -g 1263097398 --tmax 2.0

python gwemopt_plot_skymap -s ../data/S200213t/LALInference.fits.gz --fields ../data/S200213t/ZTF_fields.dat,../data/S200213t/TCA_fields.dat,../data/S200213t/TCH_fields.dat,../data/S200213t/TRE_fields.dat,../data/S200213t/OAJ_fields.dat -o ../output/S200213t_0p5 -t ZTF,TCA,TCH,TRE,OAJ -g 1265627458.327981 --tmax 0.5 

python gwemopt_plot_skymap -s ../data/S200213t/LALInference.fits.gz --fields ../data/S200213t/ZTF_fields.dat,../data/S200213t/TCA_fields.dat,../data/S200213t/TCH_fields.dat,../data/S200213t/TRE_fields.dat,../data/S200213t/OAJ_fields.dat -o ../output/S200213t_1p0 -t ZTF,TCA,TCH,TRE,OAJ -g 1265627458.327981 --tmax 1.0

python gwemopt_plot_skymap -s ../data/S200213t/LALInference.fits.gz --fields ../data/S200213t/ZTF_fields.dat,../data/S200213t/TCA_fields.dat,../data/S200213t/TCH_fields.dat,../data/S200213t/TRE_fields.dat,../data/S200213t/OAJ_fields.dat -o ../output/S200213t_2p0 -t ZTF,TCA,TCH,TRE,OAJ -g 1265627458.327981 --tmax 2.0

cp ../output/S200115j_0p5/tiles.pdf /Users/mcoughlin/Desktop/S200115j_0p5_tiles.pdf
cp ../output/S200115j_1p0/tiles.pdf /Users/mcoughlin/Desktop/S200115j_1p0_tiles.pdf
cp ../output/S200115j_2p0/tiles.pdf /Users/mcoughlin/Desktop/S200115j_2p0_tiles.pdf

cp ../output/S200213t_0p5/tiles.pdf /Users/mcoughlin/Desktop/S200213t_0p5_tiles.pdf
cp ../output/S200213t_1p0/tiles.pdf /Users/mcoughlin/Desktop/S200213t_1p0_tiles.pdf
cp ../output/S200213t_2p0/tiles.pdf /Users/mcoughlin/Desktop/S200213t_2p0_tiles.pdf

