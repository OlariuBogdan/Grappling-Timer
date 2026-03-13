import json
import os
from datetime import datetime, timedelta
import logging

class TrainingStats:
    def __init__(self, stats_file="training_stats.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()

    def load_stats(self):
        """Load training statistics from file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Error loading stats: {e}")
                return self.initialize_stats()
        else:
            return self.initialize_stats()

    def initialize_stats(self):
        """Initialize default statistics structure."""
        return {
            "total_sessions": 0,
            "total_training_time": 0,  # in seconds
            "total_rounds_completed": 0,
            "sessions": [],  # List of session records
            "weekly_stats": {},  # Weekly aggregation
            "monthly_stats": {}  # Monthly aggregation
        }

    def save_stats(self):
        """Save statistics to file."""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False, default=str)
        except IOError as e:
            logging.error(f"Error saving stats: {e}")

    def record_session(self, preset_name, work_time, rest_time, total_rounds, actual_rounds_completed, total_time):
        """Record a completed training session."""
        session = {
            "timestamp": datetime.now().isoformat(),
            "preset": preset_name,
            "work_time": work_time,
            "rest_time": rest_time,
            "planned_rounds": total_rounds,
            "completed_rounds": actual_rounds_completed,
            "total_time": total_time,
            "completion_rate": actual_rounds_completed / total_rounds if total_rounds > 0 else 0
        }

        self.stats["sessions"].append(session)
        self.stats["total_sessions"] += 1
        self.stats["total_training_time"] += total_time
        self.stats["total_rounds_completed"] += actual_rounds_completed

        # Update weekly/monthly stats
        self.update_periodic_stats(session)

        # Keep only last 1000 sessions to prevent file from growing too large
        if len(self.stats["sessions"]) > 1000:
            self.stats["sessions"] = self.stats["sessions"][-1000:]

        self.save_stats()

    def update_periodic_stats(self, session):
        """Update weekly and monthly statistics."""
        session_date = datetime.fromisoformat(session["timestamp"])
        week_key = session_date.strftime("%Y-W%W")
        month_key = session_date.strftime("%Y-%m")

        # Weekly stats
        if week_key not in self.stats["weekly_stats"]:
            self.stats["weekly_stats"][week_key] = {
                "sessions": 0,
                "total_time": 0,
                "total_rounds": 0,
                "start_date": session_date.strftime("%Y-%m-%d")
            }

        self.stats["weekly_stats"][week_key]["sessions"] += 1
        self.stats["weekly_stats"][week_key]["total_time"] += session["total_time"]
        self.stats["weekly_stats"][week_key]["total_rounds"] += session["completed_rounds"]

        # Monthly stats
        if month_key not in self.stats["monthly_stats"]:
            self.stats["monthly_stats"][month_key] = {
                "sessions": 0,
                "total_time": 0,
                "total_rounds": 0,
                "start_date": session_date.strftime("%Y-%m-%d")
            }

        self.stats["monthly_stats"][month_key]["sessions"] += 1
        self.stats["monthly_stats"][month_key]["total_time"] += session["total_time"]
        self.stats["monthly_stats"][month_key]["total_rounds"] += session["completed_rounds"]

    def get_summary(self):
        """Get a summary of training statistics."""
        total_sessions = self.stats["total_sessions"]
        total_time = self.stats["total_training_time"]
        total_rounds = self.stats["total_rounds_completed"]

        # Calculate averages
        avg_session_time = total_time / total_sessions if total_sessions > 0 else 0
        avg_rounds_per_session = total_rounds / total_sessions if total_sessions > 0 else 0

        # Recent sessions (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_sessions = [
            s for s in self.stats["sessions"]
            if datetime.fromisoformat(s["timestamp"]) > thirty_days_ago
        ]

        return {
            "total_sessions": total_sessions,
            "total_training_time": total_time,
            "total_rounds_completed": total_rounds,
            "average_session_time": avg_session_time,
            "average_rounds_per_session": avg_rounds_per_session,
            "recent_sessions_count": len(recent_sessions),
            "recent_sessions_time": sum(s["total_time"] for s in recent_sessions)
        }

    def get_weekly_progress(self, weeks=12):
        """Get weekly training progress for the last N weeks."""
        current_date = datetime.now()
        weekly_data = []

        for i in range(weeks):
            week_start = current_date - timedelta(days=current_date.weekday() + (i * 7))
            week_key = week_start.strftime("%Y-W%W")

            if week_key in self.stats["weekly_stats"]:
                weekly_data.append(self.stats["weekly_stats"][week_key])
            else:
                weekly_data.append({
                    "sessions": 0,
                    "total_time": 0,
                    "total_rounds": 0,
                    "start_date": week_start.strftime("%Y-%m-%d")
                })

        return weekly_data[::-1]  # Return in chronological order

    def export_stats(self, filename=None):
        """Export statistics to a readable format."""
        if filename is None:
            filename = f"training_stats_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        summary = self.get_summary()

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== BJJ Training Statistics ===\n\n")
            f.write(f"Total Sessions: {summary['total_sessions']}\n")
            f.write(f"Total Training Time: {self.format_time(summary['total_training_time'])}\n")
            f.write(f"Total Rounds Completed: {summary['total_rounds_completed']}\n")
            f.write(f"Average Session Time: {self.format_time(int(summary['average_session_time']))}\n")
            f.write(f"Average Rounds per Session: {summary['average_rounds_per_session']:.1f}\n")
            f.write(f"Recent Sessions (30 days): {summary['recent_sessions_count']}\n")
            f.write(f"Recent Training Time: {self.format_time(summary['recent_sessions_time'])}\n\n")

            f.write("=== Recent Sessions ===\n")
            for session in self.stats["sessions"][-10:]:  # Last 10 sessions
                f.write(f"{session['timestamp'][:10]}: {session['preset']} - {self.format_time(session['total_time'])} - {session['completed_rounds']}/{session['planned_rounds']} rounds\n")

        return filename

    @staticmethod
    def format_time(seconds):
        """Format seconds into a readable time string."""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"