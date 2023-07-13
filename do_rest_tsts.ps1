date
echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Reader IDs and name tests" 
echo ""
echo "************************************ Reader Info verification"
pytest .\Reader\readerinfo_test.py -s
echo ""
echo "************************************ Reader Name tests"
pytest .\Reader\nameset_test.py -s
echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Antenna power, dwell & sequencing tests" 
echo ""
echo "************************************ Running Dwell Tests"
pytest .\Antenna\dwell_test.py -s
echo ""
echo "************************************ Running Antenna Sequencing Tests"
pytest .\Antenna\sequence_test.py -s
echo ""
echo "************************************ Running Power Tests"
pytest .\Antenna\power_test.py -s
pytest .\Antenna\powersetall_test.py -s

echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ RAIN tests" 
echo ""
echo "************************************ Running RF Mode Tests"
pytest .\RAIN\rfmode_test.py -s
echo ""
echo "************************************ Running Q Algorithm Tests"
pytest .\RAIN\q_test.py -s
echo ""
echo "************************************ Running Select Settings Tests"
pytest .\RAIN\selectsettings_test.py -s
echo ""
echo "************************************ Running Advanced Tests"
pytest .\RAIN\advanced_test.py -s

echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ EPIC tests"
echo ""
echo "************************************ Running Tests for Setting, Deleting, and Enabling EPIC Customer Key"
pytest .\EPIC\epic_test.py -s
echo "************************************ EPIC performance tests"
echo ""
pytest .\Inventory\epicsens_test.py -s
echo ""
pytest .\Inventory\epicfast_test.py -s

echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Full profile tests" 
echo ""
echo "************************************ Running Profile Tests"
pytest .\Profile\all_test.py -s

echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Inventory tests"
echo ""
echo "************************************ Testing performance of inventory reading for different RFID settings"
echo ""
pytest .\Inventory\func1_test.py -s
echo ""
pytest .\Inventory\func2_test.py -s
echo ""
pytest .\Inventory\func3_test.py -s
echo ""
pytest .\Inventory\func4_test.py -s
echo ""
pytest .\Inventory\func5_test.py -s
echo ""
pytest .\Inventory\func6_test.py -s
echo ""
pytest .\Inventory\func7_test.py -s
echo ""
pytest .\Inventory\func8_test.py -s
echo ""
pytest .\Inventory\func10_test.py -s
echo ""
pytest .\Inventory\func11_test.py -s

echo "************************************ Expresso"
echo ""
pytest .\Inventory\expresso_test.py -s

echo "************************************ Tag filtering"
echo ""
pytest .\Inventory\filter_test.py -s
echo ""
pytest .\Inventory\filterfunc_test.py -s

echo "************************************ Access command tests"
echo ""
pytest .\Inventory\usermem_test.py -s

echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Save/Restore/Reboot tests"
echo ""
echo "************************************ Testing that data is saved and restored properly"
echo ""
pytest .\Reader\saverestore_test.py -s
echo ""
pytest .\Reader\reset_test.py -s
echo ""
pytest .\Reader\reboot_test.py -s

echo ""
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Authentication & SSL verification"
echo ""
echo "************************************ Testing authentication"
echo ""
pytest .\SSL\auth_test.py -s

echo "Done"
date