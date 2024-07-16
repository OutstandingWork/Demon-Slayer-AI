import matplotlib.pyplot as plt
import json
import argparse


def run(args):
	log_rows = []
	with open(args.in_logfile) as f:
		for line in f:
			row = json.loads(line)
			log_rows.append(row)
	log_rows = [
		row
		for row in log_rows if args.max_episode is None or
		row['episode'] <= args.max_episode]
	episodes = [row['episode'] for row in log_rows]
	losses = [row['reward'] for row in log_rows]
	# plt.plot(episodes, losses)
	# plt.savefig('vizdoom/graph.png')
	episodes_avg = []
	losses_avg = []
	average_over = 50
	num_batches = len(episodes) // average_over
	for b in range(num_batches):
		b_start = b * average_over
		b_end = b_start + average_over
		avg_episode = sum(episodes[b_start:b_end]) / average_over
		avg_loss = sum(losses[b_start:b_end]) / average_over
		episodes_avg.append(avg_episode)
		losses_avg.append(avg_loss)
	plt.plot(episodes_avg, losses_avg)
	plt.xlabel('episode')
	plt.ylabel(args.y_axis)
	plt.savefig('vizdoom/graph.png')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--in-logfile', type=str, default='log.txt')
	parser.add_argument('--max-episode', type=int)
	parser.add_argument('--y-axis', choices=['reward', 'loss'], default='reward')
	args = parser.parse_args()
	run(args)
