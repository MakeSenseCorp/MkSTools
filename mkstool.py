#!/usr/bin/python
import os
import sys
import signal
import json
import time
import thread
import threading
import argparse

from mksdk import MkSUtils
from mksdk import MkSLocalNodesCommands

Commands = MkSLocalNodesCommands.LocalNodeCommands()

parser = argparse.ArgumentParser(description='Makesense CLI tool')

parser.add_argument('-raw_data', action='store_true', default=False, 
					dest='raw_data', help='Print raw data of the request')

parser.add_argument('-m', action='store_true', default=False, 
					dest='master_commands', help='Set to master commands')

parser.add_argument('--get_master_list', action='store_true', default=False, 
					dest='get_master_list', help='Get master list command')

parser.add_argument('--get_master_nodes_info', action='store',
					dest='slave_ip_address', help='Get all nodes info for provided master')

parser.add_argument('-s', action='store_true', default=False, 
					dest='slave_commands', help='Set to slave commands')

args = parser.parse_args()

IpMasterList = None

if args.master_commands is True:
	if args.get_master_list is True:
		ips = MkSUtils.FindLocalMasterNodes()
		IpMasterList = ips
		print "\nMaster list:"
		for idx, ip in enumerate(ips):
			packet = Commands.GetMasterInfoRequest()
			raw = MkSUtils.ReadFromSocket(ip, 16999, packet)

			if "MKS" in raw[:3]:
				multiData = raw.split("MKS: ")
				for data in multiData[1:]:
					req = (data.split('\n'))[1]

				jsonData = json.loads(str(req))
				print ("  " + str(idx+1) + ". " + str(ip) + "  " + str(jsonData["info"]["hostname"]) + "  " + str(jsonData["info"]["uuid"]))
		print "\n"
	if args.slave_ip_address is not None:
		packet = Commands.GetLocalNodesRequest()
		raw = MkSUtils.ReadFromSocket(str(args.slave_ip_address), 16999, packet)

		if "MKS" in raw[:3]:
			multiData = raw.split("MKS: ")
			for data in multiData[1:]:
				req = (data.split('\n'))[1]
			jsonData = json.loads(str(req))

			print "\nNodes list:"
			for idx, node in enumerate(jsonData["nodes"]):
				print ("  " + str(idx+1) + ". " + str(node["uuid"]) + "  " + str(node["type"]) + "  " + str(node["port"]))
			print "\n"

		if args.raw_data is True:
			print("\n" + raw + "\n")
		
elif args.slave_commands is True:
	print "Slave commands"